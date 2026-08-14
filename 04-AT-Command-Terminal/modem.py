from machine import UART
import time


class EC200U:

    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):

        self.uart = UART(
            uart_id,
            baudrate=baudrate,
            tx=tx,
            rx=rx
        )

        time.sleep_ms(1000)

    def clear_buffer(self):

        while self.uart.any():
            self.uart.read()

    def send_command(self, command, timeout=3000):

        self.clear_buffer()

        command = command.strip()

        print(">>", command)

        self.uart.write(command + "\r\n")

        response = ""

        start_time = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start_time
        ) < timeout:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    response += data.decode(
                        "utf-8",
                        "ignore"
                    )

                    # Successful response
                    if "\r\nOK\r\n" in response:
                        return response.strip(), "OK"

                    # Standard AT error
                    if "\r\nERROR\r\n" in response:
                        return response.strip(), "ERROR"

                    # Quectel extended error
                    if "+CME ERROR:" in response:
                        return response.strip(), "CME ERROR"

            time.sleep_ms(20)

        if not response:
            return "NO RESPONSE", "TIMEOUT"

        return response.strip(), "TIMEOUT"

    def initialize(self):

        print()
        print("=" * 50)
        print("INITIALIZING EC200U MODEM")
        print("=" * 50)

        # Check modem communication
        response, status = self.send_command("AT")

        if status != "OK":
            print("Modem communication failed.")
            return False

        print("Modem communication: OK")

        # Disable command echo
        response, status = self.send_command("ATE0")

        if status != "OK":
            print("Failed to disable echo.")
            return False

        print("Command echo: OFF")

        print("Modem initialization complete.")

        return True

    def get_modem_info(self):

        return self.send_command("ATI")

    def get_signal(self):

        response, status = self.send_command("AT+CSQ")

        if status != "OK":
            return None, status

        try:

            line = response.split("+CSQ:")[1]
            values = line.split("\r\n")[0]

            rssi, ber = values.split(",")

            return {
                "rssi": int(rssi),
                "ber": int(ber)
            }, status

        except (IndexError, ValueError):

            return None, "PARSE ERROR"

    def get_sim_status(self):

        response, status = self.send_command("AT+CPIN?")

        if status != "OK":
            return None, status

        try:

            line = response.split("+CPIN:")[1]
            sim_status = line.split("\r\n")[0].strip()

            status_description = {
                "READY": "SIM is ready",
                "SIM PIN": "SIM requires PIN",
                "SIM PUK": "SIM requires PUK",
                "PH-NET PIN": "Network personalization PIN required",
                "PH-NET PUK": "Network personalization PUK required"
            }

            return {
                "status": sim_status,
                "description": status_description.get(
                    sim_status,
                    "Unknown SIM status"
                )
            }, status

        except (IndexError, ValueError):

            return None, "PARSE ERROR"

    def get_network_status(self):

        response, status = self.send_command("AT+CREG?")

        if status != "OK":
            return None, status

        try:

            line = response.split("+CREG:")[1]
            values = line.split("\r\n")[0]

            n, stat = values.split(",")

            stat = int(stat)

            registration_status = {
                0: "Not registered",
                1: "Registered on home network",
                2: "Searching for network",
                3: "Registration denied",
                4: "Unknown",
                5: "Registered while roaming"
            }

            return {
                "n": int(n),
                "stat": stat,
                "description": registration_status.get(
                    stat,
                    "Unknown"
                )
            }, status

        except (IndexError, ValueError):

            return None, "PARSE ERROR"

    def get_network_info(self):

        response, status = self.send_command("AT+QNWINFO")

        if status != "OK":
            return None, status

        try:

            line = response.split("+QNWINFO:")[1]
            line = line.split("\r\n")[0].strip()

            values = line.split(",")

            technology = values[0].strip('"')
            operator = values[1].strip('"')
            band = values[2].strip('"')
            channel = values[3].strip('"')

            return {
                "technology": technology,
                "operator": operator,
                "band": band,
                "channel": int(channel)
            }, status

        except (IndexError, ValueError):

            return None, "PARSE ERROR"