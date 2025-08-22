#!/usr/bin/env python3
"""
Drone Bird Deterrent System - Visual Demonstration
Aerohacks 2025

This script creates a visual simulation of the bird deterrent system in action,
showing how the system detects and responds to bird threats during a medicine delivery mission.
"""

import cv2
import numpy as np
import time
import json
import math
import random
from datetime import datetime

class DroneSimulation:
    def __init__(self):
        # Simulation parameters
        self.width = 1200
        self.height = 800
        self.fps = 30
        
        # Drone position and mission
        self.drone_pos = [100, 400]  # Starting position
        self.destination = [1100, 400]  # Destination position
        self.mission_distance = 10000  # 10km in meters
        self.current_distance = 0
        self.speed = 50  # km/h
        
        # Bird simulation
        self.birds = []
        self.bird_attack_zone = 5000  # 5km from start
        self.bird_species = ['Eagle', 'Hawk', 'Crow', 'Pigeon']
        
        # Deterrent system state
        self.system_state = "STANDBY"  # STANDBY, ALERT, ACTIVE, EMERGENCY
        self.threat_level = "NONE"     # NONE, LOW, MEDIUM, HIGH
        self.led_strobes_active = False
        self.audio_active = False
        self.detection_active = True
        
        # System metrics
        self.battery_level = 100
        self.power_consumption = 15  # Watts (standby mode)
        self.mission_time = 0
        
        # Visual elements
        self.strobe_intensity = 0
        self.audio_waves = []
        
    def create_bird(self, bird_type, distance_from_drone):
        """Create a bird object with realistic behavior"""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(20, 80)  # km/h
        
        bird = {
            'type': bird_type,
            'pos': [
                self.drone_pos[0] + distance_from_drone * math.cos(angle),
                self.drone_pos[1] + distance_from_drone * math.sin(angle)
            ],
            'velocity': [
                speed * math.cos(angle + math.pi),  # Moving towards drone
                speed * math.sin(angle + math.pi)
            ],
            'distance': distance_from_drone,
            'threat_level': self.calculate_bird_threat(bird_type, distance_from_drone),
            'detected': False,
            'confidence': random.uniform(0.7, 0.95)
        }
        
        return bird
    
    def calculate_bird_threat(self, bird_type, distance):
        """Calculate threat level based on bird type and distance"""
        threat_scores = {'Eagle': 30, 'Hawk': 20, 'Crow': 15, 'Pigeon': 5}
        base_threat = threat_scores.get(bird_type, 10)
        
        # Distance factor (closer = higher threat)
        if distance < 50:
            distance_factor = 30
        elif distance < 100:
            distance_factor = 20
        elif distance < 200:
            distance_factor = 10
        else:
            distance_factor = 0
        
        total_threat = base_threat + distance_factor
        
        if total_threat >= 40:
            return "HIGH"
        elif total_threat >= 25:
            return "MEDIUM"
        elif total_threat >= 15:
            return "LOW"
        else:
            return "NONE"
    
    def update_drone_position(self, dt):
        """Update drone position along mission path"""
        # Calculate movement
        direction = [
            self.destination[0] - self.drone_pos[0],
            self.destination[1] - self.drone_pos[1]
        ]
        distance_to_dest = math.sqrt(direction[0]**2 + direction[1]**2)
        
        if distance_to_dest > 5:  # Still moving
            # Normalize direction
            direction[0] /= distance_to_dest
            direction[1] /= distance_to_dest
            
            # Move drone
            speed_pixels_per_sec = (self.speed * 1000 / 3600) * (self.width / self.mission_distance)
            self.drone_pos[0] += direction[0] * speed_pixels_per_sec * dt
            self.drone_pos[1] += direction[1] * speed_pixels_per_sec * dt
            
            # Update mission distance
            self.current_distance = (self.drone_pos[0] - 100) / (self.width - 200) * self.mission_distance
    
    def update_birds(self, dt):
        """Update bird positions and behavior"""
        for bird in self.birds[:]:  # Copy list to allow removal
            # Update position
            bird['pos'][0] += bird['velocity'][0] * dt / 3.6  # Convert km/h to pixels/s
            bird['pos'][1] += bird['velocity'][1] * dt / 3.6
            
            # Calculate distance to drone
            dx = bird['pos'][0] - self.drone_pos[0]
            dy = bird['pos'][1] - self.drone_pos[1]
            bird['distance'] = math.sqrt(dx**2 + dy**2)
            
            # Update threat level
            bird['threat_level'] = self.calculate_bird_threat(bird['type'], bird['distance'])
            
            # Bird detection simulation
            if bird['distance'] < 300 and self.detection_active:
                bird['detected'] = True
            
            # Remove birds that are too far away
            if bird['distance'] > 500:
                self.birds.remove(bird)
    
    def update_deterrent_system(self):
        """Update deterrent system based on detected threats"""
        detected_birds = [b for b in self.birds if b['detected']]
        
        if not detected_birds:
            self.system_state = "STANDBY"
            self.threat_level = "NONE"
            self.led_strobes_active = False
            self.audio_active = False
            self.power_consumption = 15
        else:
            # Find highest threat
            max_threat = max(detected_birds, key=lambda b: 
                {'NONE': 0, 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}[b['threat_level']])
            
            self.threat_level = max_threat['threat_level']
            
            if self.threat_level == "LOW":
                self.system_state = "ALERT"
                self.led_strobes_active = True
                self.audio_active = False
                self.power_consumption = 35
            elif self.threat_level in ["MEDIUM", "HIGH"]:
                self.system_state = "ACTIVE"
                self.led_strobes_active = True
                self.audio_active = True
                self.power_consumption = 80
    
    def update_power_system(self, dt):
        """Update battery and power consumption"""
        # Calculate power consumption based on system state
        power_per_hour = self.power_consumption
        battery_drain = (power_per_hour / 3600) * dt  # Per second
        
        # Battery capacity: 3000mAh at 11.1V = 33.3Wh
        battery_capacity = 33.3
        self.battery_level -= (battery_drain / battery_capacity) * 100
        self.battery_level = max(0, self.battery_level)
    
    def draw_terrain(self, frame):
        """Draw hilly terrain background"""
        # Sky gradient
        for y in range(0, self.height // 2):
            color_intensity = int(135 + (120 * y / (self.height // 2)))
            cv2.line(frame, (0, y), (self.width, y), (color_intensity, 200, 255), 1)
        
        # Hills
        hill_points = []
        for x in range(0, self.width, 20):
            hill_height = 150 + 50 * math.sin(x * 0.01) + 30 * math.sin(x * 0.03)
            hill_points.append([x, self.height - int(hill_height)])
        
        hill_points.append([self.width, self.height])
        hill_points.append([0, self.height])
        
        cv2.fillPoly(frame, [np.array(hill_points)], (34, 139, 34))
        
        # Clouds
        for i in range(5):
            cloud_x = (i * 250 + int(self.mission_time * 10)) % (self.width + 100)
            cloud_y = 50 + i * 30
            cv2.ellipse(frame, (cloud_x, cloud_y), (60, 30), 0, 0, 360, (255, 255, 255), -1)
    
    def draw_drone(self, frame):
        """Draw the drone with deterrent system"""
        x, y = int(self.drone_pos[0]), int(self.drone_pos[1])
        
        # Drone body
        cv2.rectangle(frame, (x-20, y-10), (x+20, y+10), (100, 100, 100), -1)
        
        # Propellers
        for prop_x, prop_y in [(x-15, y-15), (x+15, y-15), (x-15, y+15), (x+15, y+15)]:
            cv2.circle(frame, (prop_x, prop_y), 8, (200, 200, 200), 2)
        
        # LED Strobes (if active)
        if self.led_strobes_active:
            self.strobe_intensity = (self.strobe_intensity + 20) % 255
            strobe_color = (255, 255, self.strobe_intensity)
            
            # Four LED strobes around drone
            for angle in [0, 90, 180, 270]:
                led_x = x + 25 * math.cos(math.radians(angle))
                led_y = y + 25 * math.sin(math.radians(angle))
                cv2.circle(frame, (int(led_x), int(led_y)), 5, strobe_color, -1)
        
        # Audio waves (if active)
        if self.audio_active:
            for radius in range(30, 100, 20):
                alpha = max(0, 100 - (radius - 30) * 2)
                cv2.circle(frame, (x, y), radius, (0, 255, 255), 2)
        
        # Medicine cargo indicator
        cv2.rectangle(frame, (x-5, y+15), (x+5, y+25), (255, 0, 0), -1)
        cv2.putText(frame, "MED", (x-10, y+35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
    
    def draw_birds(self, frame):
        """Draw birds with detection indicators"""
        for bird in self.birds:
            x, y = int(bird['pos'][0]), int(bird['pos'][1])
            
            # Bird shape (simple triangle)
            if bird['type'] == 'Eagle':
                color = (0, 100, 200)
                size = 8
            elif bird['type'] == 'Hawk':
                color = (0, 150, 150)
                size = 6
            elif bird['type'] == 'Crow':
                color = (50, 50, 50)
                size = 5
            else:  # Pigeon
                color = (100, 100, 150)
                size = 4
            
            # Draw bird
            points = np.array([[x, y-size], [x-size, y+size], [x+size, y+size]])
            cv2.fillPoly(frame, [points], color)
            
            # Detection indicator
            if bird['detected']:
                cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
                
                # Threat level indicator
                threat_colors = {
                    'LOW': (0, 255, 255),
                    'MEDIUM': (0, 165, 255),
                    'HIGH': (0, 0, 255)
                }
                
                if bird['threat_level'] in threat_colors:
                    cv2.circle(frame, (x, y), 25, threat_colors[bird['threat_level']], 3)
                
                # Distance and confidence text
                text = f"{bird['type']}: {bird['distance']:.0f}m ({bird['confidence']:.0%})"
                cv2.putText(frame, text, (x-30, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    def draw_ui(self, frame):
        """Draw user interface elements"""
        # Mission progress bar
        progress = self.current_distance / self.mission_distance
        bar_width = 300
        bar_height = 20
        bar_x, bar_y = 50, 50
        
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), 2)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
        
        # Mission info
        cv2.putText(frame, f"Mission Progress: {progress*100:.1f}% ({self.current_distance:.0f}m / {self.mission_distance}m)", 
                   (bar_x, bar_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # System status panel
        status_x, status_y = 50, 100
        cv2.rectangle(frame, (status_x, status_y), (status_x + 300, status_y + 200), (0, 0, 0), -1)
        cv2.rectangle(frame, (status_x, status_y), (status_x + 300, status_y + 200), (255, 255, 255), 2)
        
        # Status text
        status_info = [
            f"System State: {self.system_state}",
            f"Threat Level: {self.threat_level}",
            f"Battery: {self.battery_level:.1f}%",
            f"Power: {self.power_consumption}W",
            f"LED Strobes: {'ON' if self.led_strobes_active else 'OFF'}",
            f"Audio: {'ON' if self.audio_active else 'OFF'}",
            f"Birds Detected: {len([b for b in self.birds if b['detected']])}",
            f"Mission Time: {self.mission_time:.1f}s"
        ]
        
        for i, info in enumerate(status_info):
            cv2.putText(frame, info, (status_x + 10, status_y + 25 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Attack zone indicator
        attack_zone_progress = self.current_distance / self.bird_attack_zone
        if attack_zone_progress >= 0.8 and attack_zone_progress <= 1.2:
            cv2.putText(frame, "ENTERING BIRD ATTACK ZONE!", (400, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    
    def run_simulation(self):
        """Run the main simulation loop"""
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('drone_bird_deterrent_demo.mp4', fourcc, self.fps, (self.width, self.height))
        
        clock = time.time()
        
        print("Starting Drone Bird Deterrent System Simulation...")
        print("Generating demonstration video...")
        
        while self.current_distance < self.mission_distance and self.battery_level > 0:
            current_time = time.time()
            dt = current_time - clock
            clock = current_time
            
            # Create frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Update simulation
            self.mission_time += dt
            self.update_drone_position(dt)
            
            # Spawn birds in attack zone
            if (self.current_distance >= self.bird_attack_zone * 0.8 and 
                self.current_distance <= self.bird_attack_zone * 1.2 and 
                random.random() < 0.02):  # 2% chance per frame
                
                bird_type = random.choice(self.bird_species)
                distance = random.uniform(100, 300)
                self.birds.append(self.create_bird(bird_type, distance))
            
            self.update_birds(dt)
            self.update_deterrent_system()
            self.update_power_system(dt)
            
            # Draw everything
            self.draw_terrain(frame)
            self.draw_drone(frame)
            self.draw_birds(frame)
            self.draw_ui(frame)
            
            # Add title
            cv2.putText(frame, "Drone Bird Deterrent System - Aerohacks 2025", 
                       (self.width//2 - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            
            # Write frame to video
            out.write(frame)
            
            # Display frame (optional)
            cv2.imshow('Drone Bird Deterrent Simulation', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Control frame rate
            time.sleep(max(0, 1/self.fps - dt))
        
        # Cleanup
        out.release()
        cv2.destroyAllWindows()
        
        print(f"Simulation complete! Video saved as 'drone_bird_deterrent_demo.mp4'")
        print(f"Mission completed in {self.mission_time:.1f} seconds")
        print(f"Final battery level: {self.battery_level:.1f}%")
        print(f"Birds encountered: {len(self.birds)}")

if __name__ == "__main__":
    simulation = DroneSimulation()
    simulation.run_simulation()
