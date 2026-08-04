# EC200U Modem Communication using ESP32

This project demonstrates UART communication between an ESP32-WROOM-32E and the Quectel EC200U 4G LTE modem using MicroPython.

## Features

- UART communication
- AT command interface
- Read modem information
- Read firmware version
- Check signal strength
- SIM status detection

## Hardware

- ESP32-WROOM-32E
- EC200U-CN LTE Modem

## UART Configuration

- TX → GPIO17
- RX → GPIO16
- Baud Rate → 115200

## Tested Commands

- AT
- ATE0
- ATI
- AT+CPIN?
- AT+CSQ

## Output

```
Quectel
EC200U

Revision:
EC200UCNAAR02A10M08

+CSQ:12,99
```
