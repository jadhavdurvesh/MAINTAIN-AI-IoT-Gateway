# ESP32 firmware

Flash `maintain_ai_esp32.ino` with the Arduino IDE or PlatformIO.

## Default wiring

- DHT11/DHT22 data: GPIO 4
- Optional current sensor: GPIO 34
- Optional voltage sensor: GPIO 35
- Optional RPM pulse input: GPIO 27
- Serial: 115200 baud over USB

Set `ENABLE_*` flags and calibration constants in the sketch for the sensors actually connected.

The ESP32 outputs the same line-delimited JSON contract as the Arduino firmware. Connect the board by USB to the computer running the MAINTAIN AI IoT Gateway and select the serial device in the Gateway.
