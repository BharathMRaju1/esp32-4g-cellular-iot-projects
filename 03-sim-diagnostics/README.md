# Project 03 – SIM & Network Diagnostics

## ESP32 + Quectel EC200U-CN Cellular IoT Learning Series

This project demonstrates SIM initialization, SIM identification, cellular signal monitoring, network registration, operator detection, and LTE network information retrieval using an ESP32-WROOM-32E and Quectel EC200U-CN modem.

The project is developed using MicroPython and communicates with the EC200U-CN through UART using standard AT commands.

---

## Project Objective

The objective of this project is to verify the complete cellular modem bring-up sequence:

1. Establish UART communication with the EC200U-CN.
2. Verify modem responsiveness.
3. Initialize and verify the SIM card.
4. Retrieve SIM identification information.
5. Measure cellular signal strength.
6. Check network registration.
7. Check packet-domain registration.
8. Identify the cellular operator.
9. Identify the active LTE technology and band.

---

## Hardware

| Component | Specification |
|---|---|
| Development Board | GRIDBox-4G |
| Microcontroller | ESP32-WROOM-32E |
| Cellular Modem | Quectel EC200U-CN |
| SIM | Airtel LTE SIM |
| Programming Interface | PROG USB / CH340 |
| IDE | Thonny |
| Firmware | MicroPython v1.19.1 |

---

## UART Configuration

| Parameter | Value |
|---|---|
| UART | UART2 |
| Baud Rate | 115200 |
| ESP32 TX | GPIO17 |
| ESP32 RX | GPIO16 |
| Data Format | 8-N-1 |

UART connection:

```text
ESP32 GPIO17 (TX) ───────> EC200U RX

ESP32 GPIO16 (RX) <─────── EC200U TX
