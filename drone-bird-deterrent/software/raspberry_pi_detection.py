#!/usr/bin/env python3
"""
Raspberry Pi Bird Detection System
Aerohacks 2025 - Drone Bird Deterrent System

Features:
- Real-time bird detection using computer vision
- AI-powered species identification
- Distance and bearing estimation
- Communication with ESP32 main controller
"""

import cv2
import numpy as np
import tensorflow as tf
import json
import serial
import time
import threading
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BirdDetectionSystem:
    def __init__(self):
        # Camera configuration
        self.camera = None
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 30
        
        # AI Model configuration
        self.model_path = "models/bird_detection_model.tflite"
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        # Detection parameters
        self.confidence_threshold = 0.6
        self.nms_threshold = 0.4
        self.detection_classes = {
            0: "unknown",
            1: "eagle",
            2: "hawk", 
            3: "crow",
            4: "pigeon",
            5: "sparrow"
        }
        
        # Communication
        self.esp32_serial = None
        self.serial_port = "/dev/ttyAMA0"
        self.baud_rate = 115200
        
        # System state
        self.running = False
        self.detection_active = True
        self.last_detection_time = 0
        self.detection_history = []
        
        # Performance monitoring
        self.frame_count = 0
        self.start_time = time.time()
        self.processing_times = []
        
    def initialize_camera(self):
        """Initialize camera with optimal settings for bird detection"""
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure
            self.camera.set(cv2.CAP_PROP_EXPOSURE, -6)  # Fast shutter for moving objects
            
            if not self.camera.isOpened():
                raise Exception("Failed to open camera")
                
            logger.info("Camera initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            return False
    
    def initialize_ai_model(self):
        """Load and initialize TensorFlow Lite model"""
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            logger.info(f"AI model loaded: {self.model_path}")
            logger.info(f"Input shape: {self.input_details[0]['shape']}")
            logger.info(f"Output shape: {self.output_details[0]['shape']}")
            return True
            
        except Exception as e:
            logger.error(f"AI model initialization failed: {e}")
            return False
    
    def initialize_communication(self):
        """Initialize serial communication with ESP32"""
        try:
            self.esp32_serial = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=1
            )
            logger.info("ESP32 communication initialized")
            return True
            
        except Exception as e:
            logger.error(f"Communication initialization failed: {e}")
            return False
    
    def preprocess_frame(self, frame):
        """Preprocess frame for AI model input"""
        # Resize to model input size
        input_shape = self.input_details[0]['shape']
        model_height, model_width = input_shape[1], input_shape[2]
        
        # Resize and normalize
        resized = cv2.resize(frame, (model_width, model_height))
        normalized = resized.astype(np.float32) / 255.0
        
        # Add batch dimension
        input_data = np.expand_dims(normalized, axis=0)
        
        return input_data
    
    def detect_birds(self, frame):
        """Perform bird detection on input frame"""
        start_time = time.time()
        
        try:
            # Preprocess frame
            input_data = self.preprocess_frame(frame)
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            # Get detection results
            boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
            
            # Process detections
            detections = self.process_detections(boxes, classes, scores, frame.shape)
            
            # Record processing time
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
    
    def process_detections(self, boxes, classes, scores, frame_shape):
        """Process raw detection results"""
        detections = []
        height, width = frame_shape[:2]
        
        for i in range(len(scores)):
            if scores[i] > self.confidence_threshold:
                # Convert normalized coordinates to pixel coordinates
                y1 = int(boxes[i][0] * height)
                x1 = int(boxes[i][1] * width)
                y2 = int(boxes[i][2] * height)
                x2 = int(boxes[i][3] * width)
                
                # Calculate center point and size
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                box_width = x2 - x1
                box_height = y2 - y1
                
                # Estimate distance based on bounding box size
                # Larger birds (eagles) vs smaller birds (sparrows)
                estimated_distance = self.estimate_distance(box_width, box_height, int(classes[i]))
                
                # Calculate bearing from center of frame
                bearing = self.calculate_bearing(center_x, center_y, width, height)
                
                detection = {
                    'class_id': int(classes[i]),
                    'class_name': self.detection_classes.get(int(classes[i]), 'unknown'),
                    'confidence': float(scores[i]),
                    'bbox': [x1, y1, x2, y2],
                    'center': [center_x, center_y],
                    'distance': estimated_distance,
                    'bearing': bearing,
                    'timestamp': time.time()
                }
                
                detections.append(detection)
        
        return detections
    
    def estimate_distance(self, box_width, box_height, class_id):
        """Estimate distance to bird based on bounding box size and species"""
        # Average bird sizes (wingspan in cm)
        bird_sizes = {
            1: 200,  # Eagle
            2: 120,  # Hawk
            3: 90,   # Crow
            4: 60,   # Pigeon
            5: 25    # Sparrow
        }
        
        # Camera parameters (approximate)
        focal_length = 500  # pixels
        real_size = bird_sizes.get(class_id, 60)  # Default to pigeon size
        
        # Distance estimation using similar triangles
        if box_width > 0:
            distance = (real_size * focal_length) / box_width
            return min(max(distance, 10), 1000)  # Clamp between 10cm and 10m
        
        return 500  # Default distance if calculation fails
    
    def calculate_bearing(self, center_x, center_y, frame_width, frame_height):
        """Calculate bearing angle from center of frame"""
        # Camera field of view (approximate)
        horizontal_fov = 75  # degrees
        vertical_fov = 60    # degrees
        
        # Calculate offset from center
        x_offset = (center_x - frame_width / 2) / (frame_width / 2)
        y_offset = (center_y - frame_height / 2) / (frame_height / 2)
        
        # Convert to bearing angles
        horizontal_angle = x_offset * (horizontal_fov / 2)
        vertical_angle = y_offset * (vertical_fov / 2)
        
        return {
            'horizontal': horizontal_angle,
            'vertical': vertical_angle
        }
    
    def send_detection_data(self, detections):
        """Send detection data to ESP32 controller"""
        if not self.esp32_serial:
            return
        
        try:
            # Prepare data for most threatening bird
            if detections:
                # Sort by threat level (closer + larger birds = higher threat)
                threat_scores = []
                for det in detections:
                    threat_score = det['confidence'] * 100
                    threat_score += (1000 - det['distance']) / 10  # Closer = higher threat
                    if det['class_id'] in [1, 2]:  # Eagles and hawks
                        threat_score += 50
                    threat_scores.append(threat_score)
                
                # Select highest threat detection
                max_threat_idx = np.argmax(threat_scores)
                primary_detection = detections[max_threat_idx]
                
                data = {
                    'detected': True,
                    'confidence': int(primary_detection['confidence'] * 100),
                    'distance': primary_detection['distance'],
                    'bearing': primary_detection['bearing']['horizontal'],
                    'species': primary_detection['class_id'],
                    'timestamp': int(time.time() * 1000)
                }
            else:
                data = {
                    'detected': False,
                    'confidence': 0,
                    'distance': 0,
                    'bearing': 0,
                    'species': 0,
                    'timestamp': int(time.time() * 1000)
                }
            
            # Send JSON data
            json_data = json.dumps(data) + '\n'
            self.esp32_serial.write(json_data.encode())
            
        except Exception as e:
            logger.error(f"Failed to send detection data: {e}")
    
    def draw_detections(self, frame, detections):
        """Draw detection results on frame for debugging"""
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            class_name = detection['class_name']
            distance = detection['distance']
            
            # Draw bounding box
            color = (0, 255, 0) if confidence > 0.8 else (0, 255, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f} ({distance:.0f}cm)"
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame
    
    def run_detection_loop(self):
        """Main detection loop"""
        logger.info("Starting bird detection system...")
        self.running = True
        
        while self.running:
            try:
                # Capture frame
                ret, frame = self.camera.read()
                if not ret:
                    logger.warning("Failed to capture frame")
                    continue
                
                # Perform detection
                detections = self.detect_birds(frame)
                
                # Send results to ESP32
                self.send_detection_data(detections)
                
                # Update detection history
                self.detection_history.append({
                    'timestamp': time.time(),
                    'detections': len(detections),
                    'max_confidence': max([d['confidence'] for d in detections]) if detections else 0
                })
                
                # Keep only last 100 entries
                if len(self.detection_history) > 100:
                    self.detection_history.pop(0)
                
                # Performance monitoring
                self.frame_count += 1
                if self.frame_count % 100 == 0:
                    self.log_performance_stats()
                
                # Optional: Save debug frame
                if detections and len(detections) > 0:
                    debug_frame = self.draw_detections(frame.copy(), detections)
                    cv2.imwrite(f"debug_frame_{int(time.time())}.jpg", debug_frame)
                
            except Exception as e:
                logger.error(f"Detection loop error: {e}")
                time.sleep(0.1)
    
    def log_performance_stats(self):
        """Log system performance statistics"""
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        fps = self.frame_count / elapsed_time
        
        if self.processing_times:
            avg_processing_time = np.mean(self.processing_times[-100:])  # Last 100 frames
            logger.info(f"Performance: {fps:.1f} FPS, Avg processing: {avg_processing_time*1000:.1f}ms")
    
    def start(self):
        """Start the bird detection system"""
        if not self.initialize_camera():
            return False
        
        if not self.initialize_ai_model():
            return False
        
        if not self.initialize_communication():
            return False
        
        # Start detection in separate thread
        detection_thread = threading.Thread(target=self.run_detection_loop)
        detection_thread.daemon = True
        detection_thread.start()
        
        return True
    
    def stop(self):
        """Stop the bird detection system"""
        self.running = False
        
        if self.camera:
            self.camera.release()
        
        if self.esp32_serial:
            self.esp32_serial.close()
        
        logger.info("Bird detection system stopped")

def main():
    """Main function"""
    detector = BirdDetectionSystem()
    
    try:
        if detector.start():
            logger.info("Bird detection system started successfully")
            
            # Keep main thread alive
            while True:
                time.sleep(1)
                
        else:
            logger.error("Failed to start bird detection system")
            
    except KeyboardInterrupt:
        logger.info("Shutting down bird detection system...")
        detector.stop()

if __name__ == "__main__":
    main()
