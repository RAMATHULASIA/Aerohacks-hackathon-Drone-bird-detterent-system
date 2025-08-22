# Installation Guide - Drone Bird Deterrent System

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
