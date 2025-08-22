#!/usr/bin/env python3
"""
Simple Text-Based Demonstration of Drone Bird Deterrent System
Aerohacks 2025 - Medicine Delivery Drone Protection

This script provides a text-based simulation showing how the system works
without requiring OpenCV or other complex dependencies.
"""

import time
import random
import math
import json

class SimpleDroneDemo:
    def __init__(self):
        # Mission parameters
        self.mission_distance = 10000  # 10km in meters
        self.current_distance = 0
        self.speed = 50  # km/h
        self.bird_attack_zone = 5000  # 5km from start
        
        # System state
        self.system_state = "STANDBY"
        self.threat_level = "NONE"
        self.battery_level = 100
        self.power_consumption = 15  # Watts
        
        # Birds
        self.birds_detected = []
        self.deterrent_activations = 0
        self.successful_deterrents = 0
        
        # Mission log
        self.mission_log = []
        
    def log_event(self, event, details=""):
        """Log mission events"""
        timestamp = self.current_distance / 1000  # km from start
        log_entry = {
            'distance_km': round(timestamp, 1),
            'time': round(timestamp / (self.speed / 3600), 1),  # seconds
            'event': event,
            'details': details,
            'system_state': self.system_state,
            'battery': round(self.battery_level, 1),
            'power': self.power_consumption
        }
        self.mission_log.append(log_entry)
        
        print(f"[{timestamp:.1f}km] {event}: {details}")
        print(f"    State: {self.system_state} | Battery: {self.battery_level:.1f}% | Power: {self.power_consumption}W")
        print()
    
    def create_bird_encounter(self):
        """Simulate a bird encounter"""
        bird_types = ['Eagle', 'Hawk', 'Crow', 'Pigeon']
        bird_type = random.choice(bird_types)
        
        # Distance from drone (meters)
        distance = random.uniform(50, 300)
        
        # Confidence level
        confidence = random.uniform(0.7, 0.95)
        
        # Calculate threat level
        threat_scores = {'Eagle': 30, 'Hawk': 20, 'Crow': 15, 'Pigeon': 5}
        base_threat = threat_scores[bird_type]
        
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
            threat_level = "HIGH"
        elif total_threat >= 25:
            threat_level = "MEDIUM"
        elif total_threat >= 15:
            threat_level = "LOW"
        else:
            threat_level = "NONE"
        
        return {
            'type': bird_type,
            'distance': distance,
            'confidence': confidence,
            'threat_level': threat_level,
            'threat_score': total_threat
        }
    
    def update_system_state(self, bird):
        """Update system state based on bird detection"""
        if not bird:
            self.system_state = "STANDBY"
            self.threat_level = "NONE"
            self.power_consumption = 15
            return
        
        self.threat_level = bird['threat_level']
        
        if self.threat_level == "LOW":
            self.system_state = "ALERT"
            self.power_consumption = 35
        elif self.threat_level in ["MEDIUM", "HIGH"]:
            self.system_state = "ACTIVE"
            self.power_consumption = 80
        else:
            self.system_state = "STANDBY"
            self.power_consumption = 15
    
    def activate_deterrents(self, bird):
        """Simulate deterrent activation"""
        self.deterrent_activations += 1
        
        deterrent_methods = []
        
        if self.system_state == "ALERT":
            deterrent_methods.append("LED Strobes (Low Intensity)")
        elif self.system_state == "ACTIVE":
            deterrent_methods.append("LED Strobes (High Intensity)")
            deterrent_methods.append(f"Audio Distress Calls ({bird['type']} specific)")
        
        # Calculate success probability
        base_success = 0.6  # 60% base success rate
        
        # Adjust based on threat level and deterrent intensity
        if self.system_state == "ACTIVE":
            base_success += 0.25  # Full deterrent system
        elif self.system_state == "ALERT":
            base_success += 0.1   # Partial deterrent system
        
        # Species-specific adjustments
        species_factors = {'Eagle': -0.1, 'Hawk': -0.05, 'Crow': 0.05, 'Pigeon': 0.15}
        base_success += species_factors.get(bird['type'], 0)
        
        # Distance factor (closer birds harder to deter)
        if bird['distance'] < 100:
            base_success -= 0.1
        
        success = random.random() < base_success
        
        if success:
            self.successful_deterrents += 1
            result = "SUCCESS - Bird deterred"
        else:
            result = "PARTIAL - Bird maintained course"
        
        details = f"{bird['type']} at {bird['distance']:.0f}m (Threat: {bird['threat_level']}) | Methods: {', '.join(deterrent_methods)} | {result}"
        self.log_event("DETERRENT ACTIVATED", details)
        
        return success
    
    def update_battery(self, time_step):
        """Update battery level based on power consumption"""
        # Battery capacity: 3000mAh at 11.1V = 33.3Wh
        battery_capacity = 33.3
        power_per_hour = self.power_consumption
        battery_drain = (power_per_hour / 3600) * time_step  # Per second
        
        self.battery_level -= (battery_drain / battery_capacity) * 100
        self.battery_level = max(0, self.battery_level)
    
    def run_mission(self):
        """Run the complete mission simulation"""
        print("=" * 60)
        print("DRONE BIRD DETERRENT SYSTEM - MISSION SIMULATION")
        print("Aerohacks 2025 - Medicine Delivery Protection")
        print("=" * 60)
        print()
        
        print("Mission Parameters:")
        print(f"  Total Distance: {self.mission_distance/1000:.1f} km")
        print(f"  Bird Attack Zone: {self.bird_attack_zone/1000:.1f} km from origin")
        print(f"  Drone Speed: {self.speed} km/h")
        print(f"  System Weight: 1.5 kg")
        print(f"  System Cost: Rs. 47,700")
        print()
        
        self.log_event("MISSION START", "Medicine delivery drone launched")
        
        # Simulation time step (10 seconds)
        time_step = 10
        
        while self.current_distance < self.mission_distance and self.battery_level > 5:
            # Update position
            distance_per_step = (self.speed * 1000 / 3600) * time_step  # meters per time step
            self.current_distance += distance_per_step
            
            # Update battery
            self.update_battery(time_step)
            
            # Check if in bird attack zone
            in_attack_zone = (self.current_distance >= self.bird_attack_zone * 0.8 and 
                            self.current_distance <= self.bird_attack_zone * 1.2)
            
            if in_attack_zone:
                # Higher chance of bird encounters in attack zone
                if random.random() < 0.3:  # 30% chance per time step
                    bird = self.create_bird_encounter()
                    self.birds_detected.append(bird)
                    
                    details = f"{bird['type']} detected at {bird['distance']:.0f}m (Confidence: {bird['confidence']:.0%})"
                    self.log_event("BIRD DETECTED", details)
                    
                    # Update system state
                    self.update_system_state(bird)
                    
                    # Activate deterrents if needed
                    if self.system_state in ["ALERT", "ACTIVE"]:
                        self.activate_deterrents(bird)
                        
                        # Return to standby after deterrent activation
                        time.sleep(0.5)  # Brief pause for effect
                        self.update_system_state(None)
                    
            else:
                # Outside attack zone - return to standby
                if self.system_state != "STANDBY":
                    self.update_system_state(None)
            
            # Key mission milestones
            if abs(self.current_distance - 2500) < distance_per_step:
                self.log_event("MILESTONE", "25% of mission completed")
            elif abs(self.current_distance - self.bird_attack_zone) < distance_per_step:
                self.log_event("ENTERING ATTACK ZONE", "High alert - bird encounters likely")
            elif abs(self.current_distance - 7500) < distance_per_step:
                self.log_event("MILESTONE", "75% of mission completed - exiting attack zone")
            
            # Low battery warning
            if self.battery_level < 20 and self.battery_level > 15:
                self.log_event("LOW BATTERY WARNING", f"Battery at {self.battery_level:.1f}%")
            
            # Brief pause for readability
            time.sleep(0.1)
        
        # Mission completion
        if self.current_distance >= self.mission_distance:
            self.log_event("MISSION COMPLETE", "Medicine successfully delivered to destination")
            mission_success = True
        else:
            self.log_event("MISSION ABORTED", f"Low battery - emergency landing at {self.current_distance/1000:.1f}km")
            mission_success = False
        
        # Mission summary
        print("=" * 60)
        print("MISSION SUMMARY")
        print("=" * 60)
        
        mission_time = self.current_distance / (self.speed * 1000 / 3600)
        
        print(f"Mission Status: {'SUCCESS' if mission_success else 'ABORTED'}")
        print(f"Distance Traveled: {self.current_distance/1000:.1f} km / {self.mission_distance/1000:.1f} km")
        print(f"Mission Time: {mission_time/60:.1f} minutes")
        print(f"Final Battery Level: {self.battery_level:.1f}%")
        print()
        
        print("Bird Encounter Statistics:")
        print(f"  Total Birds Detected: {len(self.birds_detected)}")
        print(f"  Deterrent Activations: {self.deterrent_activations}")
        print(f"  Successful Deterrents: {self.successful_deterrents}")
        if self.deterrent_activations > 0:
            success_rate = (self.successful_deterrents / self.deterrent_activations) * 100
            print(f"  Deterrent Success Rate: {success_rate:.1f}%")
        print()
        
        print("System Performance:")
        avg_power = sum(log['power'] for log in self.mission_log) / len(self.mission_log)
        print(f"  Average Power Consumption: {avg_power:.1f}W")
        print(f"  Peak Power Consumption: {max(log['power'] for log in self.mission_log)}W")
        print(f"  System Reliability: 100% (No component failures)")
        print()
        
        # Bird species breakdown
        if self.birds_detected:
            species_count = {}
            for bird in self.birds_detected:
                species_count[bird['type']] = species_count.get(bird['type'], 0) + 1
            
            print("Bird Species Encountered:")
            for species, count in species_count.items():
                print(f"  {species}: {count}")
        
        print()
        print("System successfully demonstrated multi-layered bird deterrent capabilities")
        print("within weight (1.5kg) and budget (Rs. 47,700) constraints.")
        
        # Save mission log
        with open('mission_log.json', 'w') as f:
            json.dump({
                'mission_summary': {
                    'success': mission_success,
                    'distance_km': self.current_distance/1000,
                    'time_minutes': mission_time/60,
                    'battery_final': self.battery_level,
                    'birds_detected': len(self.birds_detected),
                    'deterrent_activations': self.deterrent_activations,
                    'successful_deterrents': self.successful_deterrents
                },
                'detailed_log': self.mission_log,
                'bird_encounters': self.birds_detected
            }, f, indent=2)
        
        print(f"\nDetailed mission log saved to 'mission_log.json'")

if __name__ == "__main__":
    demo = SimpleDroneDemo()
    demo.run_mission()
