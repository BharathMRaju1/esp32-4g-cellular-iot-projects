# Project 05 – ESP32 EC200U SMS Sender

A MicroPython-based SMS sending application using an ESP32-WROOM-32E and Quectel EC200U-CN LTE modem.

This project builds upon the UART communication, modem driver, response parsing, and diagnostic terminal developed in the previous projects.

The ESP32 communicates with the EC200U through UART and uses the modem's AT command interface to send SMS messages over the cellular network.

---

## 🎯 Objective

The objective of this project is to implement SMS sending using the Quectel EC200U-CN modem.

The project demonstrates:

- SMS text mode configuration
- GSM character-set configuration
- SMS recipient configuration
- Multi-step AT command transactions
- Modem prompt handling
- Sending SMS data through UART
- Sending the Ctrl+Z termination character
- SMS delivery response handling
- Timeout and error handling

---

## 🧰 Hardware

| Component | Details |
|---|---|
| Development Board | GRIDBox-4G |
| Microcontroller | ESP32-WROOM-32E |
| Cellular Modem | Quectel EC200U-CN |
| SIM | Airtel 4G SIM |
| Programming Port | PROG USB / CH340 |
| UART TX | GPIO17 |
| UART RX | GPIO16 |
| Baud Rate | 115200 |

---

## 💻 Software

- MicroPython v1.19.1
- Thonny IDE
- Python / MicroPython
- Quectel EC200U AT command interface

---

## 🏗️ Architecture

```text
                    ESP32
                      │
                      │ UART
                      ▼
                 modem.py
                      │
             ┌────────┴────────┐
             │                 │
        AT Commands       SMS Handler
             │                 │
             └────────┬────────┘
                      ▼
                 EC200U-CN
                      │
                      ▼
                  LTE Network
                      │
                      ▼
                 Recipient
