# GRIDBox-4G

ESP32-based 4G IoT application using the Quectel EC200U-CN cellular modem, MQTT, and Open-Meteo weather API.

## Overview

This project demonstrates cellular IoT communication using an ESP32-WROOM-32E and a Quectel EC200U-CN 4G modem.

The system can:

- Initialize and diagnose the EC200U modem
- Check SIM status
- Check cellular signal strength
- Check network registration
- Retrieve IPv4 and IPv6 addresses
- Connect to an MQTT broker
- Publish device status using JSON
- Retrieve weather information from Open-Meteo
- Publish weather information to MQTT
- Retrieve temperature information
- Use function-based architecture for different IoT operations

## Hardware

- ESP32-WROOM-32E
- GRIDBox-4G
- Quectel EC200U-CN 4G LTE modem
- SIM card
- USB/Serial programming interface

## Communication

### Cellular Network

The EC200U-CN connects to the cellular network using a SIM card.

### MQTT

The modem connects to the MQTT broker:

```text
iotrd.grid.reconnectenergy.com
