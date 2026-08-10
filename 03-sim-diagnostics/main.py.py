from machine import UART
import time


# ============================================================
# EC200U-CN SIM & Network Diagnostics
# Hardware: GRIDBox-4G
# ESP32: ESP32-WROOM-32E
# Modem: Quectel EC200U-CN
# UART: UART2
# TX: GPIO17
# RX: GPIO16
# Baudrate: 115200
# ============================================================


uart = UART(
    2,
    baudrate=115200,
    tx=17,
    rx=16
)


def send_command(command, timeout=3000):
    """
    Send an AT command to the EC200U modem
    and return its response.
    """

    # Clear old data from UART buffer
    while uart.any():
        uart.read()

    print(">>", command)

    # Send command with CRLF
    uart.write(command + "\r\n")

    start_time = time.ticks_ms()
    response = ""

    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:

        if uart.any():

            data = uart.read()

            if data:
                response += data.decode("utf-8", "ignore")

        time.sleep_ms(50)

    response = response.strip()

    if response:
        print(response)
    else:
        print("NO RESPONSE")

    print()

    return response


def run_diagnostics():

    print("=" * 40)
    print("SIM & NETWORK DIAGNOSTICS")
    print("=" * 40)

    # --------------------------------------------------------
    # Basic modem communication
    # --------------------------------------------------------

    send_command("AT")

    # Enable command echo
    send_command("ATE")

    # --------------------------------------------------------
    # SIM diagnostics
    # --------------------------------------------------------

    send_command("AT+CPIN?")

    send_command("AT+QCCID")

    send_command("AT+CCID")

    send_command("AT+CIMI")

    # --------------------------------------------------------
    # Radio / network diagnostics
    # --------------------------------------------------------

    send_command("AT+CSQ")

    send_command("AT+CREG?")

    send_command("AT+CGREG?")

    send_command("AT+COPS?")

    send_command("AT+QNWINFO")

    print("=" * 40)
    print("DIAGNOSTICS COMPLETE")
    print("=" * 40)


# Run diagnostics
run_diagnostics()