# Component Selection and Cost Analysis

## Detailed Component Specifications and Sourcing

### Detection System Components

#### 1. Camera Module
**Selected**: Raspberry Pi Camera Module 3 (12MP)
- **Specifications**:
  - Resolution: 4608×2592 pixels
  - Frame Rate: 30fps @ full resolution
  - Interface: MIPI CSI-2
  - Weight: 4.3g
  - Dimensions: 25×24×11.5mm
- **Supplier**: Element14 India
- **Cost**: Rs. 3,500
- **Justification**: High resolution for accurate bird detection, lightweight, proven reliability

#### 2. AI Processing Unit
**Selected**: Raspberry Pi 4B (4GB RAM)
- **Specifications**:
  - CPU: ARM Cortex-A72 quad-core @ 1.5GHz
  - RAM: 4GB LPDDR4
  - GPU: VideoCore VI
  - Power: 6.4W average
  - Weight: 46g
- **Supplier**: Robu.in
- **Cost**: Rs. 8,000
- **Justification**: Sufficient processing power for real-time AI inference, extensive software support

#### 3. Environmental Sensors Package
**IMU - MPU-6050**
- **Specifications**: 6-axis motion tracking
- **Supplier**: Amazon India
- **Cost**: Rs. 400

**GPS - NEO-8M Module**
- **Specifications**: 72-channel GPS receiver
- **Supplier**: Robu.in
- **Cost**: Rs. 1,200

**Barometer - BMP280**
- **Specifications**: Pressure and temperature sensing
- **Supplier**: Amazon India
- **Cost**: Rs. 400

**Total Sensors Cost**: Rs. 2,000

### Deterrent System Components

#### 1. LED Strobe Array (4 units)
**Selected**: CREE XM-L2 High-Power LEDs
- **Specifications**:
  - Power: 10W per LED
  - Luminous Flux: 1040 lumens @ 3A
  - Viewing Angle: 125°
  - Operating Temperature: -40°C to +150°C
  - Weight: 50g per unit (including driver)
- **Driver**: Constant current LED driver (3A)
- **Supplier**: LED World India
- **Cost per unit**: Rs. 2,000
- **Total Cost (4 units)**: Rs. 8,000

#### 2. Audio Deterrent System
**Speaker - Dayton Audio CE32A-4**
- **Specifications**:
  - Power: 20W RMS
  - Frequency Response: 100Hz - 8kHz
  - SPL: 110dB @ 1W/1m
  - Weather Rating: IP65
  - Weight: 180g
- **Supplier**: Prime ABGB
- **Cost**: Rs. 3,500

**Amplifier - TPA3116D2 Class D**
- **Specifications**:
  - Power Output: 30W
  - Efficiency: >90%
  - THD: <1%
  - Weight: 70g
- **Supplier**: Amazon India
- **Cost**: Rs. 2,500

**Total Audio System**: Rs. 6,000

#### 3. Visual Markers (Passive)
**Selected**: 3M Scotchlite Reflective Tape
- **Specifications**:
  - Type: Diamond Grade retroreflective
  - Width: 25mm
  - Length: 8 strips × 30cm = 2.4m total
  - Weight: 40g total
- **Supplier**: 3M India
- **Cost**: Rs. 800

### Control System Components

#### 1. Main Control Unit
**Selected**: ESP32-S3-DevKitC-1
- **Specifications**:
  - CPU: Dual-core Xtensa LX7 @ 240MHz
  - Memory: 512KB SRAM, 384KB ROM
  - Connectivity: WiFi 802.11b/g/n, Bluetooth 5.0
  - GPIO: 45 programmable pins
  - Weight: 25g
- **Supplier**: Robu.in
- **Cost**: Rs. 2,500

#### 2. Power Management System
**Battery - Tattu 3000mAh 3S LiPo**
- **Specifications**:
  - Capacity: 3000mAh
  - Voltage: 11.1V (3S configuration)
  - Discharge Rate: 25C continuous
  - Weight: 250g
- **Supplier**: Quadkopters India
- **Cost**: Rs. 3,500

**DC-DC Converters**
- **12V Rail**: LM2596 Step-down (5A capacity)
  - Cost: Rs. 300
- **5V Rail**: LM2596 Step-down (3A capacity)
  - Cost: Rs. 250
- **3.3V Rail**: AMS1117 Linear regulator (1A capacity)
  - Cost: Rs. 150

**Power Monitoring - INA219**
- **Specifications**: Current/voltage sensor
- **Cost**: Rs. 400

**Battery Management - TP4056**
- **Specifications**: LiPo charging circuit with protection
- **Cost**: Rs. 200

**Total Power System**: Rs. 4,800

#### 3. Communication System
**Selected**: LoRa SX1276 Module (915MHz)
- **Specifications**:
  - Frequency: 915MHz ISM band
  - Range: 10km+ line of sight
  - Data Rate: 5.47 kbps
  - Power: 100mW transmission
  - Weight: 15g
- **Supplier**: Robu.in
- **Cost**: Rs. 1,500

### Mechanical Components

#### 1. Mounting Hardware
**Carbon Fiber Mounting Plates**
- **Material**: 3K carbon fiber, 2mm thickness
- **Weight**: 150g
- **Cost**: Rs. 2,000

**Vibration Dampers**
- **Type**: Silicone isolators (8 pieces)
- **Weight**: 50g
- **Cost**: Rs. 500

**Fasteners and Connectors**
- **Type**: Stainless steel screws, nuts, washers
- **Weight**: 100g
- **Cost**: Rs. 800

**Total Mounting Hardware**: Rs. 3,300

#### 2. Protective Housing
**Main Enclosure**
- **Material**: ABS plastic with gasket sealing
- **Rating**: IP65
- **Weight**: 120g
- **Cost**: Rs. 1,500

**Camera Housing**
- **Material**: Transparent polycarbonate dome
- **Weight**: 35g
- **Cost**: Rs. 800

**Total Housing**: Rs. 2,300

### Development and Testing Components

#### 1. Development Tools
**Breadboards and Prototyping**
- **Cost**: Rs. 1,000

**Cables and Connectors**
- **Cost**: Rs. 1,500

**Testing Equipment Access**
- **Oscilloscope rental**: Rs. 2,000
- **Multimeter**: Rs. 500

**Total Development**: Rs. 5,000

## Cost Summary

| Category | Component | Cost (Rs.) |
|----------|-----------|------------|
| **Detection System** | | |
| | Camera Module | 3,500 |
| | AI Processing Unit | 8,000 |
| | Environmental Sensors | 2,000 |
| | **Subtotal** | **13,500** |
| **Deterrent System** | | |
| | LED Strobe Array | 8,000 |
| | Audio System | 6,000 |
| | Visual Markers | 800 |
| | **Subtotal** | **14,800** |
| **Control System** | | |
| | Main Control Unit | 2,500 |
| | Power Management | 4,800 |
| | Communication | 1,500 |
| | **Subtotal** | **8,800** |
| **Mechanical** | | |
| | Mounting Hardware | 3,300 |
| | Protective Housing | 2,300 |
| | **Subtotal** | **5,600** |
| **Development** | | |
| | Tools and Testing | 5,000 |
| | **Subtotal** | **5,000** |
| **TOTAL SYSTEM COST** | | **Rs. 47,700** |
| **Budget Remaining** | | **Rs. 2,300** |

## Weight Summary

| Category | Weight (g) |
|----------|------------|
| Detection System | 65.3 |
| Deterrent System | 490 |
| Control System | 490 |
| Mechanical Components | 455 |
| **Total System Weight** | **1,500.3g** |
| **Weight Budget** | **1,500g** |
| **Margin** | **-0.3g (within tolerance)** |

## Supplier Information

### Primary Suppliers
1. **Robu.in** - Electronics components, microcontrollers
2. **Amazon India** - Sensors, small components
3. **Element14 India** - Raspberry Pi products
4. **Quadkopters India** - Batteries and drone components
5. **3M India** - Reflective materials

### Backup Suppliers
1. **Digi-Key India** - Electronic components
2. **Mouser Electronics** - Specialized components
3. **Local Electronics Markets** - Mumbai/Delhi for urgent needs

## Risk Mitigation

### Component Availability
- **Lead Time**: 2-3 weeks for most components
- **Backup Options**: Alternative part numbers identified
- **Local Sourcing**: 80% components available locally

### Cost Fluctuation
- **Buffer**: Rs. 2,300 remaining in budget
- **Price Lock**: Quotes valid for 30 days
- **Alternatives**: Lower-cost options identified for each major component
