# Circuit Diagrams and Hardware Schematics

## System Block Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           POWER DISTRIBUTION                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ 3S LiPo     │    │ 12V Rail    │    │ 5V Rail     │    │ 3.3V Rail   │  │
│  │ 11.1V       │───▶│ LM2596      │    │ LM2596      │    │ AMS1117     │  │
│  │ 3000mAh     │    │ 5A Max      │    │ 3A Max      │    │ 1A Max      │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                   │                   │                   │       │
└─────────┼───────────────────┼───────────────────┼───────────────────┼───────┘
          │                   │                   │                   │
          ▼                   ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐
│ POWER MONITOR   │  │ LED STROBES     │  │ PROCESSING      │  │ SENSORS     │
│ • INA219        │  │ • 4x CREE XM-L2 │  │ • Raspberry Pi  │  │ • MPU-6050  │
│ • Voltage/      │  │ • LED Drivers   │  │ • ESP32-S3      │  │ • NEO-8M    │
│   Current       │  │ • PWM Control   │  │ • Camera Module │  │ • BMP280    │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘
          │                   │                   │                   │
          └───────────────────┼───────────────────┼───────────────────┘
                              │                   │
                              ▼                   ▼
                    ┌─────────────────┐  ┌─────────────────┐
                    │ AUDIO SYSTEM    │  │ COMMUNICATION   │
                    │ • 20W Speaker   │  │ • LoRa SX1276   │
                    │ • TPA3116D2 Amp │  │ • 915MHz        │
                    │ • Audio Storage │  │ • Telemetry     │
                    └─────────────────┘  └─────────────────┘
```

## Main Control Circuit

### ESP32-S3 Control Board
```
                    ESP32-S3-DevKitC-1
                   ┌─────────────────────┐
    3.3V ──────────┤ 3V3            GPIO0├──── LED Strobe 1 (PWM)
    GND ───────────┤ GND            GPIO1├──── LED Strobe 2 (PWM)
                   │                GPIO2├──── LED Strobe 3 (PWM)
    RPi UART ──────┤ GPIO43         GPIO3├──── LED Strobe 4 (PWM)
    RPi UART ──────┤ GPIO44         GPIO4├──── Audio Enable
                   │                GPIO5├──── Audio PWM
    I2C SDA ───────┤ GPIO8          GPIO6├──── LoRa CS
    I2C SCL ───────┤ GPIO9          GPIO7├──── LoRa RST
                   │               GPIO15├──── LoRa DIO0
    SPI MOSI ──────┤ GPIO11        GPIO16├──── LoRa DIO1
    SPI MISO ──────┤ GPIO13        GPIO17├──── SPI SCK
    SPI SCK ───────┤ GPIO12        GPIO18├──── SPI MOSI
                   │               GPIO21├──── Emergency Stop
    Power Mon ─────┤ GPIO14         GPIO47├──── Status LED
                   └─────────────────────┘
```

### Power Management Circuit
```
    11.1V LiPo
         │
         ├─── TP4056 Charging Circuit ─── USB-C Charging Port
         │
         ├─── Protection Circuit (Over/Under voltage, Current)
         │
         ├─── LM2596 (12V, 5A) ─── LED Strobe Array
         │         │
         │         └─── Current Sense (INA219)
         │
         ├─── LM2596 (5V, 3A) ─── Raspberry Pi 4B
         │         │              Audio Amplifier
         │         │              LoRa Module
         │         └─── Current Sense (INA219)
         │
         └─── AMS1117 (3.3V, 1A) ─── ESP32-S3
                   │                  Sensors (MPU-6050, BMP280)
                   │                  GPS Module
                   └─── Current Sense (INA219)
```

## LED Strobe Driver Circuit

### Single LED Driver (Replicate 4x)
```
    12V ────┬─── CREE XM-L2 LED (10W)
            │         │
            │         └─── Current Sense Resistor (0.1Ω)
            │                      │
    PWM ────┼─── MOSFET Driver ────┼─── N-Channel MOSFET
    (ESP32) │   (TC4427)           │   (IRFZ44N)
            │                      │
            └─── Pull-up Resistor ─┘
                 (10kΩ)
                      │
                     GND

Components per LED:
- CREE XM-L2 LED: 10W, 1040 lumens
- IRFZ44N MOSFET: 55V, 49A, RDS(on) = 17.5mΩ
- TC4427 Driver: 1.5A peak current
- 0.1Ω Current Sense: For overcurrent protection
- 10kΩ Pull-up: Ensures LED off when ESP32 not driving
```

## Audio System Circuit

### Audio Amplifier Circuit
```
    5V ─────┬─── TPA3116D2 Audio Amplifier
            │         │
    Audio ──┼─── ESP32 │ ┌─── Speaker + (20W, 4Ω)
    PWM     │    DAC   │ │
            │         │ └─── Speaker - 
            │         │
    Enable ─┼─── GPIO4 │
    (ESP32) │         │
            │         └─── Heat Sink (Thermal Management)
            │
            └─── Decoupling Capacitors
                 (100µF, 10µF, 0.1µF)

Audio Signal Chain:
ESP32 DAC → Low-pass Filter → TPA3116D2 → Speaker
         (Remove PWM noise)    (Class D Amp)
```

## Sensor Interface Circuits

### I2C Sensor Bus
```
    3.3V ────┬─── Pull-up Resistors (4.7kΩ each)
             │         │
    SDA ─────┼─────────┼─── MPU-6050 (IMU)
    SCL ─────┼─────────┼─── BMP280 (Barometer)
             │         │─── INA219 (Power Monitor 1)
             │         │─── INA219 (Power Monitor 2)
             │         └─── INA219 (Power Monitor 3)
             │
             └─── Decoupling Capacitors (0.1µF each sensor)

I2C Addresses:
- MPU-6050: 0x68
- BMP280: 0x76
- INA219 #1 (12V rail): 0x40
- INA219 #2 (5V rail): 0x41
- INA219 #3 (3.3V rail): 0x44
```

### GPS Module Interface
```
    5V ──── NEO-8M GPS Module
            │
    UART ───┼─── ESP32 GPIO (Software Serial)
    TX      │    GPIO43 (RX)
    RX      │    GPIO44 (TX)
            │
    PPS ────┼─── GPIO45 (Pulse Per Second)
            │
           GND
```

## Communication System

### LoRa Module Circuit
```
    3.3V ────┬─── SX1276 LoRa Module
             │         │
    SPI ─────┼─────────┼─── ESP32 SPI Bus
    MOSI     │         │    GPIO11 (MOSI)
    MISO     │         │    GPIO13 (MISO)
    SCK      │         │    GPIO12 (SCK)
             │         │
    CS ──────┼─────────┼─── GPIO6 (Chip Select)
    RST ─────┼─────────┼─── GPIO7 (Reset)
    DIO0 ────┼─────────┼─── GPIO15 (Interrupt)
    DIO1 ────┼─────────┼─── GPIO16 (Interrupt)
             │         │
             └─────────┴─── 915MHz Antenna (50Ω impedance)

Antenna Specifications:
- Frequency: 915MHz ±13MHz
- Gain: 2dBi omnidirectional
- VSWR: <1.5:1
- Connector: SMA or U.FL
```

## PCB Layout Considerations

### Layer Stack-up (4-layer PCB)
```
Layer 1: Component placement and signal routing
Layer 2: Ground plane (continuous)
Layer 3: Power planes (3.3V, 5V, 12V)
Layer 4: Signal routing and power distribution
```

### Design Rules
- **Trace Width**: 
  - 12V/5A: 2.0mm minimum
  - 5V/3A: 1.5mm minimum
  - 3.3V/1A: 0.8mm minimum
  - Signals: 0.2mm minimum

- **Via Size**: 0.2mm drill, 0.4mm pad
- **Clearance**: 0.15mm minimum
- **Component Spacing**: 0.5mm minimum

### Thermal Management
- **Copper Pour**: Maximum copper coverage for heat dissipation
- **Thermal Vias**: Under high-power components
- **Heat Sinks**: TPA3116D2 amplifier, LED drivers
- **Airflow**: Ventilation holes in enclosure

## Testing Points and Debug Interface

### Test Points
```
TP1: 11.1V Battery voltage
TP2: 12V Rail voltage
TP3: 5V Rail voltage  
TP4: 3.3V Rail voltage
TP5: LED Strobe current (each)
TP6: Audio amplifier current
TP7: I2C SDA signal
TP8: I2C SCL signal
TP9: UART TX (ESP32)
TP10: UART RX (ESP32)
```

### Programming Interface
- **ESP32**: USB-C connector for programming and debugging
- **Raspberry Pi**: microSD card slot for OS and software updates
- **JTAG**: 10-pin connector for advanced debugging (optional)
