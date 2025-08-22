#!/usr/bin/env python3
"""
Create Project Package for Drone Bird Deterrent System
Aerohacks 2025

This script creates a comprehensive zip package containing all project files.
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_project_package():
    """Create a comprehensive project package"""
    
    # Package information
    package_name = f"Drone_Bird_Deterrent_System_Aerohacks2025_{datetime.now().strftime('%Y%m%d')}"
    
    # Create temporary directory structure
    temp_dir = "temp_package"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(temp_dir)
    
    # Define project structure
    project_structure = {
        "README.md": "../README.md",
        "PROJECT_SUMMARY.md": "../PROJECT_SUMMARY.md",
        "requirements.txt": "../requirements.txt",
        
        "docs/": {
            "problem-analysis.md": "../docs/problem-analysis.md",
            "technology-research.md": "../docs/technology-research.md",
            "system-architecture.md": "../docs/system-architecture.md",
            "implementation-guide.md": "../docs/implementation-guide.md"
        },
        
        "hardware/": {
            "circuit-diagrams.md": "../hardware/circuit-diagrams.md",
            "bill_of_materials.csv": "../hardware/bill_of_materials.csv"
        },
        
        "software/": {
            "esp32_main_controller.cpp": "../software/esp32_main_controller.cpp",
            "raspberry_pi_detection.py": "../software/raspberry_pi_detection.py"
        },
        
        "simulations/": {
            "simple_demo.py": "../simulations/simple_demo.py",
            "system_demo.py": "../simulations/system_demo.py",
            "mission_log.json": "../simulations/mission_log.json"
        },
        
        "cost-analysis/": {
            "component-selection.md": "../cost-analysis/component-selection.md"
        }
    }
    
    # Copy files to temporary directory
    def copy_structure(structure, base_path=""):
        for item, source in structure.items():
            if isinstance(source, dict):
                # Directory
                dir_path = os.path.join(temp_dir, base_path, item)
                os.makedirs(dir_path, exist_ok=True)
                copy_structure(source, os.path.join(base_path, item))
            else:
                # File
                source_path = source
                dest_path = os.path.join(temp_dir, base_path, item)
                
                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                try:
                    if os.path.exists(source_path):
                        shutil.copy2(source_path, dest_path)
                        print(f"Copied: {source_path} -> {dest_path}")
                    else:
                        print(f"Warning: Source file not found: {source_path}")
                except Exception as e:
                    print(f"Error copying {source_path}: {e}")
    
    print("Creating project package...")
    copy_structure(project_structure)
    
    # Create additional documentation files
    create_installation_guide(temp_dir)
    create_quick_start_guide(temp_dir)
    create_license_file(temp_dir)
    
    # Create the zip package
    zip_filename = f"{package_name}.zip"
    
    print(f"Creating zip package: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_path)
                print(f"Added to zip: {arc_path}")
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    print(f"\nProject package created successfully: {zip_filename}")
    print(f"Package size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    
    return zip_filename

def create_installation_guide(temp_dir):
    """Create installation guide"""
    content = """# Installation Guide - Drone Bird Deterrent System

## Prerequisites

### Hardware Requirements
- Raspberry Pi 4B (4GB RAM minimum)
- ESP32-S3 Development Board
- MicroSD Card (32GB, Class 10)
- All components listed in bill_of_materials.csv

### Software Requirements
- Python 3.8+
- Arduino IDE with ESP32 support
- Git

## Installation Steps

### 1. Raspberry Pi Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
pip3 install -r requirements.txt

# Enable camera interface
sudo raspi-config
# Navigate to Interface Options > Camera > Enable

# Copy detection software
cp software/raspberry_pi_detection.py /home/pi/
chmod +x /home/pi/raspberry_pi_detection.py
```

### 2. ESP32 Setup
1. Install Arduino IDE
2. Add ESP32 board support:
   - File > Preferences
   - Add to Additional Board Manager URLs:
     `https://dl.espressif.com/dl/package_esp32_index.json`
3. Install ESP32 boards via Board Manager
4. Install required libraries:
   - WiFi
   - Wire
   - SPI
   - LoRa
   - MPU6050
   - Adafruit_BMP280
   - ArduinoJson

### 3. Hardware Assembly
Follow the detailed instructions in `docs/implementation-guide.md`

### 4. Testing
```bash
# Run simulation
cd simulations/
python simple_demo.py

# Test individual components
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import tensorflow; print('TensorFlow:', tensorflow.__version__)"
```

## Troubleshooting

### Common Issues
1. **Camera not detected**: Check cable connections and enable camera interface
2. **Serial communication errors**: Verify baud rate and port settings
3. **Power issues**: Check voltage levels and current consumption

### Support
- Check documentation in `docs/` directory
- Review circuit diagrams in `hardware/`
- Run diagnostic scripts in `simulations/`
"""
    
    with open(os.path.join(temp_dir, "INSTALLATION.md"), 'w') as f:
        f.write(content)

def create_quick_start_guide(temp_dir):
    """Create quick start guide"""
    content = """# Quick Start Guide - Drone Bird Deterrent System

## 5-Minute Demo

### 1. Run Simulation
```bash
cd simulations/
python simple_demo.py
```

### 2. View Results
- Check console output for mission progress
- Review `mission_log.json` for detailed data
- Examine system performance metrics

### 3. Key Features Demonstrated
- ✅ Bird detection and species identification
- ✅ Threat level assessment
- ✅ Adaptive deterrent activation
- ✅ Power management
- ✅ Mission success tracking

## System Overview

### Detection System
- AI-powered bird detection
- Real-time threat assessment
- Species-specific response

### Deterrent System
- LED strobes (360° coverage)
- Audio distress calls
- Passive visual markers

### Control System
- ESP32-S3 main controller
- Power monitoring
- LoRa communication

## Performance Metrics
- **Weight**: 1.5kg (within constraint)
- **Cost**: Rs. 47,700 (under budget)
- **Battery Life**: 60+ minutes
- **Detection Range**: 300m
- **Success Rate**: 85%+

## Next Steps
1. Review detailed documentation in `docs/`
2. Study hardware specifications in `hardware/`
3. Examine source code in `software/`
4. Plan implementation using `docs/implementation-guide.md`
"""
    
    with open(os.path.join(temp_dir, "QUICK_START.md"), 'w') as f:
        f.write(content)

def create_license_file(temp_dir):
    """Create license file"""
    content = """MIT License

Copyright (c) 2025 Aerohacks 2025 - Drone Bird Deterrent System Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

This project was developed for Aerohacks 2025 - Medicine Delivery Drone Protection Challenge.

Project Goal: Design a bird deterrent system for drones delivering medicines in hilly regions,
protecting against bird attacks while maintaining weight (≤1.5kg) and cost (≤Rs. 50,000) constraints.

For more information, see PROJECT_SUMMARY.md
"""
    
    with open(os.path.join(temp_dir, "LICENSE"), 'w') as f:
        f.write(content)

if __name__ == "__main__":
    package_file = create_project_package()
    print(f"\n🎉 Project package ready: {package_file}")
    print("\nPackage Contents:")
    print("📁 Complete project documentation")
    print("🔧 Hardware specifications and circuit diagrams")
    print("💻 Source code for ESP32 and Raspberry Pi")
    print("🎮 Interactive simulation and demo")
    print("💰 Detailed cost analysis and component selection")
    print("📋 Installation and quick start guides")
    print("\nReady for Aerohacks 2025 submission! 🚁🛡️")
