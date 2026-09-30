# Maintain AI Firmware

This folder contains reference firmware for physical sensor nodes that connect to the **MAINTAIN AI IoT Gateway** over USB serial.

The firmware is intentionally gateway-oriented: the microcontroller reads sensors and emits one JSON telemetry object per line. The Gateway owns authentication, machine pairing, buffering, retries, and HTTPS upload to Maintain AI.

## Supported examples

- `arduino/maintain_ai_arduino.ino` — Arduino Mega/Uno-class boards using serial output. Configure the sensor blocks at the top of the file.
- `esp32/maintain_ai_esp32.ino` — ESP32 using USB serial output. It uses the same serial contract, so the same Gateway can receive either board.

## Serial contract

Each reading is one JSON object terminated by `\\n`, for example:

```json
{"reading_type":"temperature","value":29.30,"unit":"C"}
{"reading_type":"humidity","value":57.20,"unit":"%"}
```

The Gateway adds the device identity, timestamp/event metadata as required by its transport contract, and sends the readings to the Maintain AI ingest API.

## Sensor flexibility

The examples are deliberately structured around small `readSensors()` functions. To add a sensor:

1. Include its Arduino library if required.
2. Configure its pins/address near the top of the sketch.
3. Read it inside `readSensors()`.
4. Call `sendReading("<Maintain AI signal>", value, "<unit>")`.

Use signal names accepted by the Gateway's canonical signal catalog, such as `temperature`, `humidity`, `vibration`, `current`, `voltage`, `pressure`, `flow`, `speed`, `load`, `rpm`, `motor_current`, `motor_temperature`, `spindle_rpm`, `spindle_load`, `nozzle_temperature`, `bed_temperature`, and `chamber_temperature`.

## Important

Do not put Supabase credentials, Vercel credentials, or the Gateway device key into these sketches. Device authentication belongs in the Gateway application. The microcontroller only needs to produce sensor readings.
