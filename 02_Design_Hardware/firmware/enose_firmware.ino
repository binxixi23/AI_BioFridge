/*
================================================================================
AI_BIOFRIDGE: MULTI-SENSOR ELECTRONIC NOSE (E-NOSE) FIRMWARE
================================================================================
Target Hardware: Arduino Uno, Nano, or ESP32
Description: Reads real-time voltage variations from gas sensor arrays,
             calculates chemical baseline scales, and streams telemetry via Serial.
================================================================================
*/

// Define Microcontroller Analog Pins connected to the E-Nose sensors
const int MQ135_PIN = A0;  // Detects Ammonia, Benzene, Alcohol, Smoke, and general VOCs
const int MQ4_PIN   = A1;  // Detects Methane (CH4) and organic Ethylene ripening gases

// Calibration constants (Vary based on your environmental background room air)
const float Ro_MQ135 = 10.0; // Base resistance in clean air
const float Ro_MQ4   = 10.0; // Base resistance in clean air
const float V_REF    = 5.0;  // Operating voltage (Use 3.3 for ESP32)

void setup() {
  // Initialize high-speed hardware serial communication to pass data to the Python AI master
  Serial.begin(115200);
  
  // Give the heated sensor coils time to preheat and stabilize internally (Simulation skip)
  Serial.println("{\"status\": \"E-Nose Preheating Coils Stabilizing...\"}");
  delay(2000); 
}

void loop() {
  // 1. Read raw digital integers from 10-bit Analog-to-Digital Converter (0 to 1023)
  int raw_mq135 = analogRead(MQ135_PIN);
  int raw_mq4   = analogRead(MQ4_PIN);

  // 2. Convert raw values into actual electrical voltage values
  float volt_mq135 = (raw_mq135 * V_REF) / 1023.0;
  float volt_mq4   = (raw_mq4 * V_REF) / 1023.0;

  // 3. Approximate sensor resistance calculation profiles (Rs)
  // Formula: Rs = (Vcc - V_sensor) / V_sensor
  float rs_mq135 = (V_REF - volt_mq135) / volt_mq135;
  float rs_mq4   = (V_REF - volt_mq4) / volt_mq4;

  // 4. Calculate relative pollution concentration scale ratios (Rs/Ro)
  float ratio_mq135 = rs_mq135 / Ro_MQ135;
  float ratio_mq4   = rs_mq4 / Ro_MQ4;

  // 5. Structure telemetry into a clean, safe JSON payload string for the Python parser
  Serial.print("{");
  Serial.print("\"device\":\"E_NOSE_BOARD\",");
  Serial.print("\"mq135_volt\":" + String(volt_mq135, 2) + ",");
  Serial.print("\"mq4_volt\":" + String(volt_mq4, 2) + ",");
  Serial.print("\"ammonia_voc_ratio\":" + String(ratio_mq135, 2) + ",");
  Serial.print("\"ethylene_methane_ratio\":" + String(ratio_mq4, 2));
  Serial.println("}");

  // Sample the air chemistry variables every 1000 milliseconds (1 second loops)
  delay(1000);
}
