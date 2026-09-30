/*
 * Maintain AI - flexible Arduino telemetry node
 *
 * Board: Arduino Uno/Mega-class boards
 * Link: USB serial -> MAINTAIN AI IoT Gateway
 *
 * The Arduino does NOT authenticate to Maintain AI. It emits JSON readings;
 * the Gateway handles device identity, buffering, retries and HTTPS upload.
 *
 * Default sensors:
 *   - DHT11/DHT22 temperature + humidity
 *   - optional analog current sensor
 *   - optional analog voltage sensor
 *   - optional digital RPM pulse input
 *
 * Set the ENABLE_* flags and pins below for your hardware.
 */

#include <Arduino.h>
#include <DHT.h>

// ---------- Board / serial ----------
#define SERIAL_BAUD 115200

// ---------- DHT ----------
#define ENABLE_DHT 1
#define DHT_PIN 4
#define DHT_TYPE DHT11   // Change to DHT22 when required
DHT dht(DHT_PIN, DHT_TYPE);

// ---------- Analog sensors ----------
#define ENABLE_ANALOG_CURRENT 0
#define CURRENT_PIN A0
#define CURRENT_SCALE 1.0f
#define CURRENT_OFFSET 0.0f

#define ENABLE_ANALOG_VOLTAGE 0
#define VOLTAGE_PIN A1
#define VOLTAGE_SCALE 1.0f
#define VOLTAGE_OFFSET 0.0f

// ---------- RPM pulse sensor ----------
#define ENABLE_RPM 0
#define RPM_PIN 2
#define RPM_PULSES_PER_REV 1.0f

// ---------- Sampling ----------
const unsigned long TELEMETRY_INTERVAL_MS = 5000;
unsigned long lastTelemetryMs = 0;
volatile unsigned long pulseCount = 0;

void onRpmPulse() {
  pulseCount++;
}

void sendReading(const char* readingType, float value, const char* unit) {
  if (!isfinite(value)) return;

  Serial.print("{\"reading_type\":\"");
  Serial.print(readingType);
  Serial.print("\",\"value\":");
  Serial.print(value, 3);
  Serial.print(",\"unit\":\"");
  Serial.print(unit);
  Serial.println("\"}");
}

void readSensors() {
#if ENABLE_DHT
  const float temperature = dht.readTemperature();
  const float humidity = dht.readHumidity();

  if (!isnan(temperature)) {
    sendReading("temperature", temperature, "C");
  }
  if (!isnan(humidity)) {
    sendReading("humidity", humidity, "%");
  }
#endif

#if ENABLE_ANALOG_CURRENT
  const float raw = (float)analogRead(CURRENT_PIN);
  const float current = raw * CURRENT_SCALE + CURRENT_OFFSET;
  sendReading("current", current, "A");
#endif

#if ENABLE_ANALOG_VOLTAGE
  const float raw = (float)analogRead(VOLTAGE_PIN);
  const float voltage = raw * VOLTAGE_SCALE + VOLTAGE_OFFSET;
  sendReading("voltage", voltage, "V");
#endif

#if ENABLE_RPM
  noInterrupts();
  const unsigned long pulses = pulseCount;
  pulseCount = 0;
  interrupts();

  const float sampleSeconds = TELEMETRY_INTERVAL_MS / 1000.0f;
  const float rpm = (pulses / RPM_PULSES_PER_REV) * (60.0f / sampleSeconds);
  sendReading("rpm", rpm, "rpm");
#endif
}

void setup() {
  Serial.begin(SERIAL_BAUD);

#if ENABLE_DHT
  dht.begin();
#endif

#if ENABLE_RPM
  pinMode(RPM_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(RPM_PIN), onRpmPulse, RISING);
#endif

  delay(500);
  Serial.println("MAINTAIN_AI_SENSOR_NODE_READY");
}

void loop() {
  const unsigned long now = millis();
  if (now - lastTelemetryMs < TELEMETRY_INTERVAL_MS) return;
  lastTelemetryMs = now;

  readSensors();
}
