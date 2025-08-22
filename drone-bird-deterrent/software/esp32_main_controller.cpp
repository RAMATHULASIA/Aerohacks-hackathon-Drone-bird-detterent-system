/*
 * ESP32-S3 Main Controller for Drone Bird Deterrent System
 * Aerohacks 2025 - Medicine Delivery Drone Protection
 * 
 * Features:
 * - Multi-sensor integration (IMU, GPS, Barometer)
 * - LED strobe control with PWM
 * - Audio deterrent system
 * - LoRa communication for telemetry
 * - Power monitoring and management
 * - AI-driven threat response system
 */

#include <WiFi.h>
#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <MPU6050.h>
#include <Adafruit_BMP280.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

// Pin Definitions
#define LED_STROBE_1    0
#define LED_STROBE_2    1
#define LED_STROBE_3    2
#define LED_STROBE_4    3
#define AUDIO_ENABLE    4
#define AUDIO_PWM       5
#define LORA_CS         6
#define LORA_RST        7
#define I2C_SDA         8
#define I2C_SCL         9
#define LORA_DIO0       15
#define LORA_DIO1       16
#define EMERGENCY_STOP  21
#define STATUS_LED      47
#define RPI_UART_RX     43
#define RPI_UART_TX     44

// System States
enum SystemState {
  STATE_STANDBY,
  STATE_ALERT,
  STATE_ACTIVE,
  STATE_EMERGENCY
};

enum ThreatLevel {
  THREAT_NONE,
  THREAT_LOW,
  THREAT_MEDIUM,
  THREAT_HIGH
};

// Global Variables
SystemState currentState = STATE_STANDBY;
ThreatLevel currentThreat = THREAT_NONE;
unsigned long lastTelemetryTime = 0;
unsigned long lastSensorUpdate = 0;
unsigned long deterrentActivationTime = 0;
bool emergencyStop = false;

// Sensor Objects
MPU6050 mpu;
Adafruit_BMP280 bmp;
SoftwareSerial gpsSerial(RPI_UART_RX, RPI_UART_TX);
SoftwareSerial rpiSerial(RPI_UART_RX, RPI_UART_TX);

// Sensor Data Structure
struct SensorData {
  float accelX, accelY, accelZ;
  float gyroX, gyroY, gyroZ;
  float temperature;
  float pressure;
  float altitude;
  float gpsLat, gpsLon;
  bool gpsValid;
  float batteryVoltage;
  float systemCurrent;
  unsigned long timestamp;
};

SensorData sensors;

// Power Monitoring
struct PowerData {
  float voltage12V, current12V, power12V;
  float voltage5V, current5V, power5V;
  float voltage3V3, current3V3, power3V3;
  float totalPower;
  float batteryLevel;
};

PowerData powerStatus;

// Bird Detection Data from Raspberry Pi
struct BirdDetection {
  bool detected;
  int confidence;
  float distance;
  float bearing;
  int species;
  unsigned long timestamp;
};

BirdDetection birdData;

void setup() {
  Serial.begin(115200);
  Serial.println("Drone Bird Deterrent System - Initializing...");
  
  // Initialize GPIO pins
  initializeGPIO();
  
  // Initialize I2C sensors
  initializeSensors();
  
  // Initialize LoRa communication
  initializeLoRa();
  
  // Initialize audio system
  initializeAudio();
  
  // Initialize LED strobes
  initializeLEDStrobes();
  
  // Set initial state
  currentState = STATE_STANDBY;
  
  Serial.println("System initialization complete - Ready for operation");
  digitalWrite(STATUS_LED, HIGH);
}

void loop() {
  // Check emergency stop
  if (digitalRead(EMERGENCY_STOP) == LOW) {
    emergencyStop = true;
    currentState = STATE_EMERGENCY;
  }
  
  // Update sensor data (10Hz)
  if (millis() - lastSensorUpdate >= 100) {
    updateSensorData();
    lastSensorUpdate = millis();
  }
  
  // Check for bird detection from Raspberry Pi
  checkBirdDetection();
  
  // Update system state based on threat assessment
  updateSystemState();
  
  // Control deterrent systems based on current state
  controlDeterrents();
  
  // Monitor power consumption
  monitorPowerSystems();
  
  // Send telemetry data (1Hz)
  if (millis() - lastTelemetryTime >= 1000) {
    sendTelemetryData();
    lastTelemetryTime = millis();
  }
  
  // System health monitoring
  performHealthCheck();
  
  delay(50); // 20Hz main loop
}

void initializeGPIO() {
  // LED Strobe pins
  pinMode(LED_STROBE_1, OUTPUT);
  pinMode(LED_STROBE_2, OUTPUT);
  pinMode(LED_STROBE_3, OUTPUT);
  pinMode(LED_STROBE_4, OUTPUT);
  
  // Audio control pins
  pinMode(AUDIO_ENABLE, OUTPUT);
  pinMode(AUDIO_PWM, OUTPUT);
  
  // Status and emergency pins
  pinMode(STATUS_LED, OUTPUT);
  pinMode(EMERGENCY_STOP, INPUT_PULLUP);
  
  // Initialize PWM channels for LED strobes
  ledcSetup(0, 1000, 8); // Channel 0, 1kHz, 8-bit resolution
  ledcSetup(1, 1000, 8); // Channel 1
  ledcSetup(2, 1000, 8); // Channel 2
  ledcSetup(3, 1000, 8); // Channel 3
  
  ledcAttachPin(LED_STROBE_1, 0);
  ledcAttachPin(LED_STROBE_2, 1);
  ledcAttachPin(LED_STROBE_3, 2);
  ledcAttachPin(LED_STROBE_4, 3);
}

void initializeSensors() {
  Wire.begin(I2C_SDA, I2C_SCL);
  
  // Initialize MPU6050 IMU
  if (mpu.begin()) {
    Serial.println("MPU6050 initialized successfully");
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  } else {
    Serial.println("Failed to initialize MPU6050");
  }
  
  // Initialize BMP280 Barometer
  if (bmp.begin()) {
    Serial.println("BMP280 initialized successfully");
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                    Adafruit_BMP280::SAMPLING_X2,
                    Adafruit_BMP280::SAMPLING_X16,
                    Adafruit_BMP280::FILTER_X16,
                    Adafruit_BMP280::STANDBY_MS_500);
  } else {
    Serial.println("Failed to initialize BMP280");
  }
  
  // Initialize GPS communication
  gpsSerial.begin(9600);
  rpiSerial.begin(115200);
}

void initializeLoRa() {
  LoRa.setPins(LORA_CS, LORA_RST, LORA_DIO0);
  
  if (LoRa.begin(915E6)) {
    Serial.println("LoRa initialized successfully");
    LoRa.setSpreadingFactor(12);
    LoRa.setSignalBandwidth(125E3);
    LoRa.setCodingRate4(8);
    LoRa.setTxPower(20);
  } else {
    Serial.println("Failed to initialize LoRa");
  }
}

void initializeAudio() {
  digitalWrite(AUDIO_ENABLE, LOW); // Start with audio disabled
  
  // Initialize PWM for audio control
  ledcSetup(4, 44100, 8); // Channel 4, 44.1kHz for audio
  ledcAttachPin(AUDIO_PWM, 4);
  
  Serial.println("Audio system initialized");
}

void initializeLEDStrobes() {
  // Turn off all LED strobes initially
  ledcWrite(0, 0);
  ledcWrite(1, 0);
  ledcWrite(2, 0);
  ledcWrite(3, 0);
  
  Serial.println("LED strobe system initialized");
}

void updateSensorData() {
  sensors.timestamp = millis();
  
  // Read IMU data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  sensors.accelX = a.acceleration.x;
  sensors.accelY = a.acceleration.y;
  sensors.accelZ = a.acceleration.z;
  sensors.gyroX = g.gyro.x;
  sensors.gyroY = g.gyro.y;
  sensors.gyroZ = g.gyro.z;
  
  // Read barometer data
  sensors.temperature = bmp.readTemperature();
  sensors.pressure = bmp.readPressure();
  sensors.altitude = bmp.readAltitude(1013.25); // Sea level pressure
  
  // Read GPS data (simplified - would need full NMEA parsing)
  if (gpsSerial.available()) {
    // Parse GPS data here
    sensors.gpsValid = true; // Placeholder
  }
  
  // Read battery voltage (through voltage divider)
  int adcValue = analogRead(A0);
  sensors.batteryVoltage = (adcValue * 3.3 / 4095.0) * 4.0; // Voltage divider ratio
}

void checkBirdDetection() {
  if (rpiSerial.available()) {
    String jsonData = rpiSerial.readStringUntil('\n');
    
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonData);
    
    if (!error) {
      birdData.detected = doc["detected"];
      birdData.confidence = doc["confidence"];
      birdData.distance = doc["distance"];
      birdData.bearing = doc["bearing"];
      birdData.species = doc["species"];
      birdData.timestamp = millis();
      
      // Assess threat level based on detection data
      assessThreatLevel();
    }
  }
}

void assessThreatLevel() {
  if (!birdData.detected) {
    currentThreat = THREAT_NONE;
    return;
  }
  
  // Threat assessment algorithm
  int threatScore = 0;
  
  // Distance factor (closer = higher threat)
  if (birdData.distance < 50) threatScore += 30;
  else if (birdData.distance < 100) threatScore += 20;
  else if (birdData.distance < 200) threatScore += 10;
  
  // Confidence factor
  threatScore += birdData.confidence / 10;
  
  // Species factor (eagles and hawks more dangerous)
  if (birdData.species == 1) threatScore += 20; // Eagle
  else if (birdData.species == 2) threatScore += 15; // Hawk
  else if (birdData.species == 3) threatScore += 10; // Crow
  
  // Determine threat level
  if (threatScore >= 50) currentThreat = THREAT_HIGH;
  else if (threatScore >= 30) currentThreat = THREAT_MEDIUM;
  else if (threatScore >= 15) currentThreat = THREAT_LOW;
  else currentThreat = THREAT_NONE;
}

void updateSystemState() {
  if (emergencyStop) {
    currentState = STATE_EMERGENCY;
    return;
  }
  
  switch (currentThreat) {
    case THREAT_NONE:
      currentState = STATE_STANDBY;
      break;
    case THREAT_LOW:
      currentState = STATE_ALERT;
      break;
    case THREAT_MEDIUM:
    case THREAT_HIGH:
      currentState = STATE_ACTIVE;
      deterrentActivationTime = millis();
      break;
  }
}

void controlDeterrents() {
  switch (currentState) {
    case STATE_STANDBY:
      // All deterrents off, passive visual markers only
      setLEDStrobes(0);
      setAudioDeterrent(false);
      break;
      
    case STATE_ALERT:
      // Low-intensity LED strobes
      setLEDStrobes(50); // 20% intensity
      setAudioDeterrent(false);
      break;
      
    case STATE_ACTIVE:
      // Full deterrent activation
      setLEDStrobes(255); // 100% intensity
      setAudioDeterrent(true);
      
      // Auto-deactivate after 60 seconds to conserve power
      if (millis() - deterrentActivationTime > 60000) {
        currentState = STATE_ALERT;
      }
      break;
      
    case STATE_EMERGENCY:
      // Minimal power consumption mode
      setLEDStrobes(0);
      setAudioDeterrent(false);
      break;
  }
}

void setLEDStrobes(int intensity) {
  // Create strobe pattern with phase offset for 360° coverage
  unsigned long time = millis();
  float timeRad = (time % 1000) * 2.0 * PI / 1000.0;

  int phase1 = (sin(timeRad) + 1.0) * intensity / 2;
  int phase2 = (sin(timeRad + PI/2) + 1.0) * intensity / 2;
  int phase3 = (sin(timeRad + PI) + 1.0) * intensity / 2;
  int phase4 = (sin(timeRad + 3*PI/2) + 1.0) * intensity / 2;

  ledcWrite(0, phase1);
  ledcWrite(1, phase2);
  ledcWrite(2, phase3);
  ledcWrite(3, phase4);
}

void setAudioDeterrent(bool enable) {
  digitalWrite(AUDIO_ENABLE, enable);
  
  if (enable) {
    // Generate distress call pattern (simplified)
    int frequency = 2000 + sin(millis() * 0.01) * 500;
    ledcWriteTone(4, frequency);
  } else {
    ledcWriteTone(4, 0);
  }
}

void monitorPowerSystems() {
  // Read power monitoring data from INA219 sensors
  // This would interface with actual INA219 modules
  powerStatus.totalPower = powerStatus.power12V + powerStatus.power5V + powerStatus.power3V3;
  
  // Calculate battery level based on voltage
  float minVoltage = 9.0; // 3S LiPo minimum safe voltage
  float maxVoltage = 12.6; // 3S LiPo maximum voltage
  powerStatus.batteryLevel = (sensors.batteryVoltage - minVoltage) / (maxVoltage - minVoltage) * 100;
  
  // Low battery warning
  if (powerStatus.batteryLevel < 30) {
    Serial.println("WARNING: Low battery level");
  }
}

void sendTelemetryData() {
  DynamicJsonDocument doc(1024);
  
  doc["timestamp"] = millis();
  doc["state"] = currentState;
  doc["threat"] = currentThreat;
  doc["battery"] = powerStatus.batteryLevel;
  doc["power"] = powerStatus.totalPower;
  doc["altitude"] = sensors.altitude;
  doc["temperature"] = sensors.temperature;
  
  if (birdData.detected) {
    doc["bird_detected"] = true;
    doc["bird_confidence"] = birdData.confidence;
    doc["bird_distance"] = birdData.distance;
  }
  
  String telemetryString;
  serializeJson(doc, telemetryString);
  
  // Send via LoRa
  LoRa.beginPacket();
  LoRa.print(telemetryString);
  LoRa.endPacket();
}

void performHealthCheck() {
  // System health monitoring
  static unsigned long lastHealthCheck = 0;
  
  if (millis() - lastHealthCheck >= 5000) { // Every 5 seconds
    // Check sensor connectivity
    // Check power levels
    // Check communication status
    // Log any issues
    
    lastHealthCheck = millis();
  }
}
