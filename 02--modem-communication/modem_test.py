from machine import UART
import time

# UART2 on GPIO17 (TX) and GPIO16 (RX)
uart = UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=17, rx=16)

def send(cmd):
    print(">>", cmd)

    # Clear any old data
    while uart.any():
        uart.read()

    uart.write(cmd + "\r\n")

    time.sleep(2)

    if uart.any():
        data = uart.read()
        print(data.decode("utf-8", "ignore"))
    else:
        print("No Response")

print("=" * 40)
print("EC200U Communication Test")
print("=" * 40)

send("AT")
send("ATE0")
send("ATI")
send("AT+CPIN?")
send("AT+CSQ")