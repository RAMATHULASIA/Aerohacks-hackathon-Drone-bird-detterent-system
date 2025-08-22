# System Architecture - Drone Bird Deterrent System

## System Overview

### Core Design Philosophy
**Multi-Layered Defense**: Combining passive and active deterrents for maximum effectiveness
**Smart Activation**: AI-driven threat assessment to optimize power usage
**Modular Design**: Easy integration with various drone platforms
**Weather Resilience**: IP65-rated components for harsh environmental conditions

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DRONE PLATFORM                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   DETECTION     │  │   DETERRENT     │  │   CONTROL   │ │
│  │    SYSTEM       │  │    SYSTEM       │  │   SYSTEM    │ │
│  │                 │  │                 │  │             │ │
│  │ • Camera Module │  │ • LED Strobes   │  │ • Main MCU  │ │
│  │ • AI Processor  │  │ • Audio System  │  │ • Power Mgmt│ │
│  │ • Sensors       │  │ • Visual Markers│  │ • Telemetry │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│           │                     │                   │      │
│           └─────────────────────┼───────────────────┘      │
│                                 │                          │
│  ┌─────────────────────────────────────────────────────────┤
│  │              POWER DISTRIBUTION SYSTEM                  │
│  │  • 3000mAh LiPo Battery  • DC-DC Converters            │
│  │  • Power Monitoring      • Emergency Backup            │
│  └─────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

## Subsystem Specifications

### 1. Detection System

#### Primary Camera Module
- **Model**: Raspberry Pi Camera Module 3 (12MP)
- **Resolution**: 4608×2592 @ 30fps
- **Field of View**: 75° diagonal
- **Weight**: 4.3g
- **Power**: 2.5W
- **Cost**: Rs. 3,500

#### AI Processing Unit
- **Model**: Raspberry Pi 4B (4GB RAM)
- **Processing**: ARM Cortex-A72 quad-core
- **AI Framework**: TensorFlow Lite
- **Weight**: 46g
- **Power**: 6.4W (average)
- **Cost**: Rs. 8,000

#### Environmental Sensors
- **IMU**: MPU-6050 (gyroscope + accelerometer)
- **GPS**: NEO-8M module
- **Barometer**: BMP280
- **Total Weight**: 15g
- **Total Power**: 1.5W
- **Total Cost**: Rs. 2,000

### 2. Deterrent System

#### LED Strobe Array (4 units)
- **Model**: High-intensity white LEDs (10W each)
- **Configuration**: 90° spacing for 360° coverage
- **Flash Rate**: 60 flashes/minute (adjustable)
- **Visibility**: 2km+ in clear conditions
- **Weight**: 200g (50g × 4)
- **Power**: 40W peak, 8W average
- **Cost**: Rs. 8,000 (Rs. 2,000 × 4)

#### Audio Deterrent System
- **Speaker**: 20W weatherproof speaker
- **Amplifier**: Class D amplifier (30W)
- **Audio Library**: 50+ bird distress calls
- **Frequency Range**: 100Hz - 8kHz
- **Sound Level**: 110dB @ 1m
- **Weight**: 250g
- **Power**: 25W peak, 5W average
- **Cost**: Rs. 6,000

#### Visual Markers (Passive)
- **Type**: Reflective tape strips (8 units)
- **Material**: 3M Scotchlite retroreflective
- **Length**: 30cm each
- **Weight**: 40g total
- **Power**: 0W (passive)
- **Cost**: Rs. 800

### 3. Control System

#### Main Control Unit
- **Microcontroller**: ESP32-S3 (dual-core, WiFi/Bluetooth)
- **Memory**: 512KB SRAM, 384KB ROM
- **Storage**: 32GB microSD card
- **Interfaces**: UART, SPI, I2C, PWM
- **Weight**: 25g
- **Power**: 3W average
- **Cost**: Rs. 2,500

#### Power Management System
- **Battery**: 3000mAh 3S LiPo (11.1V nominal)
- **DC-DC Converters**: 
  - 12V rail (LED strobes): 5A capacity
  - 5V rail (electronics): 3A capacity
  - 3.3V rail (sensors): 1A capacity
- **Power Monitoring**: INA219 current/voltage sensors
- **Weight**: 450g
- **Cost**: Rs. 5,000

#### Communication System
- **Telemetry**: 915MHz LoRa module
- **Range**: 10km+ line of sight
- **Data Rate**: 5.47 kbps
- **Weight**: 15g
- **Power**: 2W
- **Cost**: Rs. 1,500

## System Integration

### Mounting Configuration
```
     [Camera]
        │
    [LED] ─ [DRONE] ─ [LED]
        │     │
    [Audio]   │
        │  [Control]
    [LED] ─ [Battery] ─ [LED]
```

### Weight Distribution
- **Detection System**: 65.3g
- **Deterrent System**: 490g
- **Control System**: 490g
- **Mounting Hardware**: 300g
- **Protective Housing**: 154.7g
- **Total System Weight**: 1,500g (exactly at limit)

### Power Budget
- **Standby Mode**: 15W (detection only)
- **Alert Mode**: 35W (detection + visual)
- **Active Mode**: 80W (full system)
- **Mission Profile**: 
  - Standby: 70% of flight time
  - Alert: 20% of flight time
  - Active: 10% of flight time
- **Average Power**: 28W
- **Flight Time**: 60+ minutes

## Operational Modes

### 1. Standby Mode (Default)
- Camera monitoring active
- Passive visual markers deployed
- Power consumption: 15W
- All deterrents on standby

### 2. Alert Mode (Bird Detected)
- LED strobes activate (low intensity)
- Audio system armed
- Increased camera frame rate
- Power consumption: 35W

### 3. Active Mode (Threat Imminent)
- Full LED strobe intensity
- Audio distress calls active
- Evasive maneuver capability
- Power consumption: 80W
- Duration: 30-60 seconds max

### 4. Emergency Mode (System Failure)
- Basic visual deterrents only
- Minimal power consumption
- Safe return to base protocol
- Power consumption: 10W

## Environmental Protection

### Weatherproofing
- **Enclosure Rating**: IP65 (dust-tight, water-resistant)
- **Operating Temperature**: -10°C to +50°C
- **Humidity**: 0-95% non-condensing
- **Vibration Resistance**: 5G operational, 15G survival

### Shock Protection
- **Vibration Dampers**: Silicone isolators for sensitive components
- **Protective Housing**: Carbon fiber reinforced polymer
- **Component Securing**: Conformal coating on PCBs

## Fail-Safe Mechanisms

### Redundancy
- **Dual Power Rails**: Critical systems on separate power buses
- **Backup Detection**: Multiple sensor fusion for threat detection
- **Manual Override**: Ground control can activate deterrents

### Emergency Protocols
- **Low Battery**: Automatic return-to-base at 30% charge
- **System Failure**: Graceful degradation to passive deterrents
- **Communication Loss**: Pre-programmed deterrent activation zones
