# MAINTAIN AI IoT Gateway

[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/jadhavdurvesh/MAINTAIN-AI-IoT-Gateway)

MAINTAIN AI IoT Gateway is a lightweight desktop gateway that connects wired industrial devices and sensor controllers to the MAINTAIN AI cloud platform over HTTPS.

## Architecture

```text
Industrial Device / Controller + Sensors
                  ↓ USB / Serial
          MAINTAIN AI IoT Gateway
                  ↓ HTTPS
          MAINTAIN AI Backend
                  ↓
               Machine
                  ↓
     Sensor readings / analytics /
     anomaly detection / alerts
```

The gateway is an IoT connectivity layer. It is not a replacement for the main MAINTAIN AI application.

## Device support

The gateway is designed around a generic serial-device interface rather than being tied to a specific controller brand. Arduino boards are supported, but they are only one possible hardware source.

Multiple serial devices can be connected to the same gateway at the same time, with each device maintaining its own:

- Serial connection
- Machine pairing
- Device key
- Connection status
- Live readings
- Upload status

## Current target

- Automatic serial-device detection and port selection
- Configurable baud rate
- One JSON object per line
- Temperature, humidity and other supported sensor readings
- Machine-specific IoT device keys
- HTTPS upload to `/api/devices/ingest`
- Connection and backend status
- Live sensor readings
- Basic logging
- Multiple simultaneous serial devices
- Windows desktop application and installer

The first hardware demonstration uses a DH11-style temperature/humidity sensor connected to an Arduino Mega. The production gateway is not limited to this hardware.

## Backend

Production API:

`https://maintain-ai-3.vercel.app/api/devices/ingest`

Each upload uses the machine's IoT device key through:

`X-Device-Key: <machine-device-key>`

The gateway must not use worker login credentials for device ingestion.

## Roadmap

### Milestone 1

Serial device + JSON + live HTTPS upload.

### Milestone 2

Desktop UI, automatic device detection, validation, retry logic, offline store-and-forward queue, persistent configuration, secure credential storage, and multiple connected devices.

### Milestone 3

Windows installer, system tray/background mode, auto-start, multiple sensor profiles, protocol versioning, diagnostics, and broader controller support.

## Development

Python is the first implementation language.

- Serial: `pyserial`
- HTTP: `requests`
- Desktop UI: `PySide6`
- Local queue: SQLite or a lightweight durable queue
- Packaging: PyInstaller
- Installer: Inno Setup

Build incrementally. Do not redesign the MAINTAIN AI backend; use the existing device ingestion endpoint and machine-specific device key.
