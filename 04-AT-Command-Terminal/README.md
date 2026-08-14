# Project 04 – ESP32 EC200U AT Command Terminal

A MicroPython-based interactive AT command terminal and basic modem driver for the **Quectel EC200U-CN LTE modem**, running on an **ESP32-WROOM-32E** through UART.

This project builds upon the UART communication developed in Project 02 and introduces modem initialization, response handling, error detection, command abstraction, and response parsing.

---

## 📌 Project Overview

The goal of this project is to develop a reusable MicroPython interface for communicating with the Quectel EC200U-CN cellular modem.

Instead of directly writing UART commands throughout the application, the project introduces a dedicated modem driver that handles:

- UART communication
- AT command transmission
- Response reception
- Timeout handling
- Error detection
- Modem initialization
- Response parsing
- SIM status
- Signal information
- Network registration
- LTE network information

The project also provides an interactive terminal that allows the user to enter both custom AT commands and predefined diagnostic commands.

---

## 🎯 Objectives

By completing this project, the following concepts were implemented:

- Understand AT command communication
- Communicate with a cellular modem using UART
- Implement a reusable modem driver
- Handle modem responses
- Detect `OK`, `ERROR`, and `CME ERROR`
- Implement communication timeouts
- Initialize the EC200U automatically
- Disable AT command echo using `ATE0`
- Parse modem responses into structured Python data
- Create application-level modem commands
- Build a reusable foundation for future cellular IoT projects

---

## 🧰 Hardware

| Component | Details |
|---|---|
| Microcontroller | ESP32-WROOM-32E |
| Development Board | GRIDBox-4G |
| Cellular Modem | Quectel EC200U-CN |
| Programming Interface | PROG USB / CH340 |
| SIM | Airtel 4G SIM |
| UART TX | GPIO17 |
| UART RX | GPIO16 |
| Baud Rate | 115200 |

---

## 💻 Software

- MicroPython v1.19.1
- Thonny IDE
- Python / MicroPython
- UART / AT command interface

---

## 🔌 UART Configuration

The ESP32 communicates with the EC200U using UART.

```text
ESP32                    EC200U-CN
-----------------------------------
GPIO17 TX  ------------> RX
GPIO16 RX  <------------ TX
GND        ------------> GND 
```

---

EXAMPLE OUTPUT

=============================================
EC200U AT COMMAND TERMINAL
=============================================

=============================================
INITIALIZING EC200U MODEM
=============================================
>> AT
Modem communication: OK
>> ATE0
Command echo: OFF
Modem initialization complete.

Available commands:
  modem   - Modem information
  signal  - Signal information
  sim     - SIM status
  network - Network registration
  nwinfo  - LTE network information
  EXIT    - Exit terminal

You can also enter any AT command.
==================================================

---

Modem information

AT> modem
>> ATI
Quectel
EC200U
Revision: EC200UCNAAR02A10M08

OK
STATUS: OK

---

Signal

AT> signal
>> AT+CSQ
Signal Information

RSSI: 14
BER : 99
STATUS: OK

---

SIM

AT> sim
>> AT+CPIN?
SIM Status

Status : READY
Result : SIM is ready
STATUS : OK

---

Network

AT> network
>> AT+CREG?
Network Registration

Mode   : 0
Status : 1
Result : Registered on home network
STATUS : OK

---

LTE network

AT> nwinfo
>> AT+QNWINFO
Network Information

Technology : FDD LTE
Operator   : 40445
Band       : LTE BAND 3
Channel    : 1301
STATUS     : OK
