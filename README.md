# MAINTAIN AI IoT Gateway

MAINTAIN AI IoT Gateway is a lightweight desktop gateway that connects wired Arduino-based sensors to the MAINTAIN AI cloud platform over HTTPS.

## Architecture

```text
Arduino + Sensors
      ↓ USB / Serial
MAINTAIN AI IoT Gateway
      ↓ HTTPS
MAINTAIN AI Backend
      ↓
Machine
      ↓
Sensor readings / analytics / anomaly detection / alerts
```

The gateway is an IoT connectivity layer. It is not a replacement for the main MAINTAIN AI application.

## Current target

The first working version will support:

- Arduino serial detection and COM-port selection
- 115200 baud serial communication
- One JSON object per line
- Temperature and humidity readings
- Machine-specific IoT device key
- HTTPS upload to `/api/devices/ingest`
- Connection status
- Live sensor readings
- Basic logging

The first hardware demonstration uses a DH11-style temperature/humidity sensor connected to an Arduino Mega.

## Backend

Production API:

`https://maintain-ai-3.vercel.app/api/devices/ingest`

Each upload uses the machine's IoT device key through:

`X-Device-Key: <machine-device-key>`

The gateway must not use worker login credentials for device ingestion.

## Roadmap

### Milestone 1

Arduino USB serial + JSON + live HTTPS upload.

### Milestone 2

PySide6 desktop UI, automatic port detection, validation, retry logic, offline store-and-forward queue, persistent configuration, and secure credential storage.

### Milestone 3

Windows installer, system tray/background mode, auto-start, multiple sensors, protocol versioning, and diagnostics.

## Development direction

Python is the first implementation language.

- Serial: `pyserial`
- HTTP: `requests`
- Desktop UI: `PySide6`
- Local queue: SQLite or a lightweight durable queue
- Packaging: PyInstaller

Build incrementally. Do not redesign the MAINTAIN AI backend; use the existing device ingestion endpoint and machine-specific device key.
