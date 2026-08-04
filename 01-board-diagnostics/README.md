# ESP32 Board Diagnostics

A MicroPython-based board diagnostics utility for the ESP32-WROOM-32E. This project verifies the development environment and retrieves essential hardware information before starting embedded IoT development.

---

## Overview

This project collects and displays important system information from the ESP32, making it useful as an initial hardware validation step.

The program retrieves:

- Board Information
- Chip Name
- Firmware Version
- CPU Frequency
- Flash Memory Size
- Available RAM
- Reset Cause
- Wake-up Reason

---

## Hardware

- ESP32-WROOM-32E
- USB CH340 Interface

---

## Software

- MicroPython v1.19.1
- Thonny IDE

---

## Sample Output

```text
========================================
GRIDBox-4G Board Diagnostics
========================================

Board        : ESP32 module with ESP32
Chip         : esp32
Firmware     : 1.19.1
Version      : v1.19.1 on 2022-06-18

CPU Frequency: 160 MHz
Flash Size   : 4 MB
Free RAM     : 108880 Bytes

Reset Cause  : 5
Wake Reason  : 0

========================================
```

---

## Project Structure

```
01-board-diagnostics/
│
├── main.py
├── README.md
├── LICENSE
└── images/
    └── output.png
```

---

## Skills Demonstrated

- Embedded Systems
- MicroPython
- ESP32 Hardware Diagnostics
- Memory Management
- Flash Memory Detection
- CPU Configuration
- System Information Retrieval

---

## Future Improvements

- Chip Temperature Monitoring
- GPIO Status Scanner
- UART Detection
- Wi-Fi Status Check
- Battery Voltage Monitoring

---

## Author

**Bharath M**

Electronics and Communication Engineer

Learning Embedded Systems | IoT | Python Automation
