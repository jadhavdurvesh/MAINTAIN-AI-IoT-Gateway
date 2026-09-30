# Arduino firmware

Flash `maintain_ai_arduino.ino` with the Arduino IDE.

## Default wiring

- DHT11/DHT22 data: digital pin 4
- Optional current sensor: A0
- Optional voltage sensor: A1
- Optional RPM pulse input: digital pin 2
- Serial: 115200 baud over USB

The sketch is intentionally configurable at the top. Enable only the sensors that are physically connected and adjust calibration constants for the sensor module.

Connect the Arduino by USB to the computer running the MAINTAIN AI IoT Gateway. The Gateway consumes the line-delimited JSON readings and handles cloud authentication/upload.
