from machine import UART
import time
import json


class EC200U:

    def __init__(self):

        # ==========================================
        # UART
        # ==========================================

        self.uart = UART(
            2,
            baudrate=115200,
            tx=17,
            rx=16,
            timeout=1000
        )

        # ==========================================
        # DEVICE
        # ==========================================

        self.device_name = "GRIDBox-01"
        self.modem_name = "Quectel EC200U-CN"

        # ==========================================
        # MQTT
        # ==========================================

        self.broker = "iotrd.grid.reconnectenergy.com"
        self.port = 1883

        self.username = "username"
        self.password = "password"

        self.topic = "test/test/test/test"

        self.mqtt_opened = False
        self.mqtt_connected = False

        # ==========================================
        # WEATHER
        # ==========================================

        self.weather_host = "api.open-meteo.com"
        self.weather_port = 80

        self.weather_path = (
            "/v1/forecast"
            "?latitude=12.9719"
            "&longitude=77.5937"
            "&current="
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "wind_speed_10m,"
            "weather_code,"
            "rain"
        )

        # ==========================================
        # UPTIME
        # ==========================================

        self.start_time = time.ticks_ms()

    # ==================================================
    # CLEAR UART
    # ==================================================

    def clear_buffer(self):

        while self.uart.any():

            self.uart.read()

    # ==================================================
    # SEND AT COMMAND
    # ==================================================

    def send_at(self, command, wait=2):

        self.clear_buffer()

        print("AT>", command)

        self.uart.write(
            command + "\r\n"
        )

        response = b""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < wait * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:
                    response += data

            time.sleep_ms(50)

        try:

            text = response.decode()

        except:

            text = str(response)

        print(">>", text)

        return text

    # ==================================================
    # INITIALIZE MODEM
    # ==================================================

    def initialize(self):

        print("")
        print("========================================")
        print("EC200U INITIALIZATION")
        print("========================================")

        self.send_at("AT")
        self.send_at("ATE0")
        self.send_at("AT+CFUN?")
        self.send_at("AT+CPIN?")
        self.send_at("AT+CSQ")
        self.send_at("AT+CREG?")
        self.send_at("AT+CGREG?")
        self.send_at("AT+CGPADDR=1")

    # ==================================================
    # SIGNAL
    # ==================================================

    def get_signal(self):

        response = self.send_at(
            "AT+CSQ"
        )

        rssi = None
        ber = None

        try:

            for line in response.splitlines():

                if "+CSQ:" in line:

                    value = line.split(":")[1].strip()

                    parts = value.split(",")

                    rssi = int(parts[0])
                    ber = int(parts[1])

        except:

            pass

        return {
            "rssi": rssi,
            "ber": ber
        }

    # ==================================================
    # SIM STATUS
    # ==================================================

    def get_sim_status(self):

        response = self.send_at(
            "AT+CPIN?"
        )

        if "+CPIN: READY" in response:

            return "READY"

        return "UNKNOWN"

    # ==================================================
    # NETWORK
    # ==================================================

    def get_network_info(self):

        return self.send_at(
            "AT+QNWINFO"
        )

    # ==================================================
    # IP ADDRESS
    # ==================================================

    def get_ip_address(self):

        response = self.send_at(
            "AT+CGPADDR=1"
        )

        ipv4 = None
        ipv6 = None

        try:

            for line in response.splitlines():

                if "+CGPADDR:" in line:

                    value = line.split(
                        ",",
                        1
                    )[1]

                    value = value.strip()
                    value = value.strip('"')

                    parts = value.split(",")

                    if len(parts) >= 1:
                        ipv4 = parts[0]

                    if len(parts) >= 2:
                        ipv6 = parts[1]

        except:

            pass

        return {
            "ipv4": ipv4,
            "ipv6": ipv6
        }

    # ==================================================
    # BATTERY
    # ==================================================

    def get_battery(self):

        response = self.send_at(
            "AT+CBC"
        )

        voltage = None
        percentage = None

        try:

            for line in response.splitlines():

                if "+CBC:" in line:

                    value = line.split(":")[1]

                    parts = value.split(",")

                    percentage = int(
                        parts[1]
                    )

                    voltage = int(
                        parts[2]
                    ) / 1000

        except:

            pass

        return {
            "voltage": voltage,
            "percentage": percentage
        }

    # ==================================================
    # MQTT CONFIG
    # ==================================================

    def mqtt_config(self):

        print("")
        print("========================================")
        print("MQTT CONFIGURATION")
        print("========================================")

        self.send_at(
            'AT+QMTCFG="version",0,4'
        )

        self.send_at(
            'AT+QMTCFG="keepalive",0,60'
        )

        self.send_at(
            'AT+QMTCFG="ssl",0,0'
        )

        print("MQTT configuration complete.")

    # ==================================================
    # MQTT OPEN
    # ==================================================

    def mqtt_open(self):

        print("")
        print("========================================")
        print("MQTT OPEN")
        print("========================================")

        self.clear_buffer()

        command = (
            'AT+QMTOPEN=0,"{}",{}'
            .format(
                self.broker,
                self.port
            )
        )

        print("AT>", command)

        self.uart.write(
            command + "\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 30 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if "+QMTOPEN: 0,0" in response:

                        self.mqtt_opened = True

                        return True

                    if "+QMTOPEN: 0,2" in response:

                        return False

            time.sleep_ms(100)

        return False

    # ==================================================
    # MQTT CONNECT
    # ==================================================

    def mqtt_connect(self):

        if not self.mqtt_opened:

            return False

        self.clear_buffer()

        command = (
            'AT+QMTCONN=0,"{}","{}"'
            .format(
                self.username,
                self.password
            )
        )

        print("AT>", command)

        self.uart.write(
            command + "\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 20 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if "+QMTCONN: 0,0,0" in response:

                        self.mqtt_connected = True

                        return True

            time.sleep_ms(100)

        return False

    # ==================================================
    # MQTT STATUS
    # ==================================================

    def check_mqtt_status(self):

        response = self.send_at(
            "AT+QMTCONN?",
            5
        )

        if "+QMTCONN: 0,0" in response:

            self.mqtt_connected = True

            return True

        self.mqtt_connected = False

        return False

    # ==================================================
    # ENSURE MQTT
    # ==================================================

    def ensure_mqtt(self):

        print("")
        print("########################################")
        print("#           ENSURE MQTT")
        print("########################################")

        # ------------------------------------------
        # Already connected?
        # ------------------------------------------

        if self.check_mqtt_status():

            print("MQTT ALREADY CONNECTED")

            return True

        # ------------------------------------------
        # Configure
        # ------------------------------------------

        print("MQTT NOT CONNECTED")

        self.mqtt_config()

        # ------------------------------------------
        # Open broker
        # ------------------------------------------

        if not self.mqtt_open():

            print("MQTT OPEN FAILED")

            return False

        # ------------------------------------------
        # Connect
        # ------------------------------------------

        if not self.mqtt_connect():

            print("MQTT CONNECTION FAILED")

            return False

        print("MQTT READY")

        return True

    # ==================================================
    # MQTT PUBLISH
    # ==================================================

    def publish(self, message):

        if not self.mqtt_connected:

            print("MQTT NOT CONNECTED")

            return False

        print("")
        print("========================================")
        print("MQTT PUBLISH")
        print("========================================")

        print("Topic:", self.topic)
        print("Message:", message)

        command = (
            'AT+QMTPUB=0,0,0,0,"{}"'
            .format(self.topic)
        )

        self.clear_buffer()

        self.uart.write(
            command + "\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 10 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if ">" in response:

                        break

            time.sleep_ms(50)

        if ">" not in response:

            print("MQTT PROMPT FAILED")

            return False

        self.uart.write(
            message + "\x1A"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 15 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if "+QMTPUB:" in response:

                        break

            time.sleep_ms(50)

        if "+QMTPUB: 0,0,0" in response:

            print("PUBLISHED SUCCESSFULLY")

            return True

        print("PUBLISH FAILED")

        return False

    # ==================================================
    # DEVICE STATUS
    # ==================================================

    def get_device_status(self):

        signal = self.get_signal()
        battery = self.get_battery()
        sim = self.get_sim_status()
        ip = self.get_ip_address()
        network = self.get_network_info()

        uptime = (
            time.ticks_diff(
                time.ticks_ms(),
                self.start_time
            )
            // 1000
        )

        return {

            "ip": ip,

            "device": self.device_name,

            "signal": signal,

            "battery": battery,

            "mqtt": {
                "connected":
                    self.mqtt_connected,

                "topic":
                    self.topic,

                "broker":
                    self.broker
            },

            "modem":
                self.modem_name,

            "uptime_seconds":
                uptime,

            "sim":
                sim,

            "network":
                network
        }

    # ==================================================
    # PUBLISH DEVICE STATUS
    # ==================================================

    def publish_device_status(self):

        data = self.get_device_status()

        message = json.dumps(data)

        print("")
        print("JSON MESSAGE:")
        print(message)

        return self.publish(message)

    # ==================================================
    # CLOSE WEATHER SOCKET
    # ==================================================

    def close_weather_socket(self):

        print("")
        print("Closing weather socket...")

        self.send_at(
            "AT+QICLOSE=0",
            5
        )

    # ==================================================
    # OPEN WEATHER TCP
    # ==================================================

    def open_weather_socket(self):

        print("")
        print("========================================")
        print("OPENING WEATHER TCP CONNECTION")
        print("========================================")

        # ------------------------------------------
        # Make sure socket 0 is free
        # ------------------------------------------

        self.clear_buffer()

        self.uart.write(
            "AT+QICLOSE=0\r\n"
        )

        time.sleep_ms(1000)

        self.clear_buffer()

        # ------------------------------------------
        # Open TCP
        # ------------------------------------------

        command = (
            'AT+QIOPEN=1,0,"TCP","{}",{}'
            .format(
                self.weather_host,
                self.weather_port
            )
        )

        print("AT>", command)

        self.uart.write(
            command + "\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 30 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if "+QIOPEN: 0,0" in response:

                        print(
                            "TCP CONNECTION OPEN"
                        )

                        return True

                    if "+QIOPEN: 0," in response:

                        if "+QIOPEN: 0,0" not in response:

                            print(
                                "WEATHER TCP OPEN FAILED"
                            )

                            return False

            time.sleep_ms(100)

        print(
            "WEATHER TCP OPEN TIMEOUT"
        )

        return False

    # ==================================================
    # SEND WEATHER HTTP REQUEST
    # ==================================================

    def send_weather_request(self):

        request = (
            "GET {} HTTP/1.1\r\n"
            "Host: {}\r\n"
            "Connection: close\r\n"
            "User-Agent: GRIDBox-01\r\n"
            "\r\n"
        ).format(
            self.weather_path,
            self.weather_host
        )

        print("")
        print("HTTP REQUEST:")
        print(request)

        length = len(request)

        command = (
            "AT+QISEND=0,{}"
            .format(length)
        )

        print("AT>", command)

        self.clear_buffer()

        self.uart.write(
            command + "\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 10 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if ">" in response:

                        break

            time.sleep_ms(50)

        if ">" not in response:

            print("QISEND PROMPT FAILED")

            return False

        # ------------------------------------------
        # Send actual HTTP request
        # ------------------------------------------

        self.uart.write(request)

        print("HTTP REQUEST SENT")

        return True

    # ==================================================
    # READ WEATHER SOCKET
    # ==================================================

    def read_weather_socket(self):

        print("")
        print("WAITING FOR WEATHER RESPONSE")

        complete_response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 30 * 1000:

            # --------------------------------------
            # Check UART
            # --------------------------------------

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    print(">>", text)

                    complete_response += text

                    # ----------------------------------
                    # Server says data arrived
                    # ----------------------------------

                    if (
                        '+QIURC: "recv",0'
                        in complete_response
                    ):

                        print(
                            "WEATHER DATA RECEIVED"
                        )

                        # ----------------------------------
                        # Read socket
                        # ----------------------------------

                        time.sleep_ms(500)

                        read_response = self.read_socket_data()

                        if read_response:

                            complete_response += (
                                read_response
                            )

                        # ----------------------------------
                        # Check whether JSON exists
                        # ----------------------------------

                        if "{" in complete_response:

                            return complete_response

            time.sleep_ms(100)

        print(
            "WEATHER RESPONSE TIMEOUT"
        )

        return complete_response

    # ==================================================
    # READ SOCKET DATA USING QIRD
    # ==================================================

    def read_socket_data(self):

        print("")
        print("READING SOCKET DATA")

        self.clear_buffer()

        self.uart.write(
            "AT+QIRD=0\r\n"
        )

        response = ""

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < 10 * 1000:

            if self.uart.any():

                data = self.uart.read()

                if data:

                    try:

                        text = data.decode()

                    except:

                        text = str(data)

                    response += text

                    print(">>", text)

                    if "\r\nOK\r\n" in response:

                        break

            time.sleep_ms(50)

        return response

    # ==================================================
    # EXTRACT JSON
    # ==================================================

    def extract_json(self, response):

        start_index = response.find("{")

        end_index = response.rfind("}")

        if start_index == -1:

            print(
                "WEATHER JSON NOT FOUND"
            )

            return None

        if end_index == -1:

            print(
                "WEATHER JSON INCOMPLETE"
            )

            return None

        json_text = response[
            start_index:
            end_index + 1
        ]

        print("")
        print("WEATHER JSON:")
        print(json_text)

        return json_text

    # ==================================================
    # WEATHER CODE
    # ==================================================

    def weather_code_to_text(self, code):

        if code == 0:
            return "Clear Sky"

        if code in [1, 2, 3]:
            return "Cloudy"

        if code in [45, 48]:
            return "Fog"

        if code in [51, 53, 55]:
            return "Drizzle"

        if code in [61, 63, 65]:
            return "Rain"

        if code in [66, 67]:
            return "Freezing Rain"

        if code in [71, 73, 75]:
            return "Snow"

        if code in [80, 81, 82]:
            return "Rain Showers"

        if code == 95:
            return "Thunderstorm"

        if code in [96, 99]:
            return "Thunderstorm With Hail"

        return "UNKNOWN"

    # ==================================================
    # GET WEATHER
    # ==================================================

    def get_weather(self):

        print("")
        print("========================================")
        print("GETTING WEATHER")
        print("========================================")

        # ------------------------------------------
        # Open TCP
        # ------------------------------------------

        if not self.open_weather_socket():

            return None

        # ------------------------------------------
        # Send request
        # ------------------------------------------

        if not self.send_weather_request():

            self.close_weather_socket()

            return None

        # ------------------------------------------
        # Read response
        # ------------------------------------------

        response = self.read_weather_socket()

        # ------------------------------------------
        # Close socket
        # ------------------------------------------

        self.close_weather_socket()

        # ------------------------------------------
        # Extract JSON
        # ------------------------------------------

        json_text = self.extract_json(
            response
        )

        if json_text is None:

            return None

        # ------------------------------------------
        # Parse JSON
        # ------------------------------------------

        try:

            data = json.loads(
                json_text
            )

            current = data.get(
                "current",
                {}
            )

            weather = {

                "location":
                    "Bengaluru",

                "temperature":
                    current.get(
                        "temperature_2m"
                    ),

                "feels_like":
                    current.get(
                        "apparent_temperature"
                    ),

                "humidity":
                    current.get(
                        "relative_humidity_2m"
                    ),

                "wind_speed":
                    current.get(
                        "wind_speed_10m"
                    ),

                "rain":
                    current.get(
                        "rain"
                    ),

                "weather_code":
                    current.get(
                        "weather_code"
                    ),

                "condition":
                    self.weather_code_to_text(
                        current.get(
                            "weather_code"
                        )
                    )
            }

            print("")
            print("WEATHER DATA:")
            print(weather)

            return weather

        except Exception as e:

            print(
                "WEATHER JSON ERROR:",
                e
            )

            return None

    # ==================================================
    # TEMPERATURE FUNCTION
    # ==================================================

    def get_temperature(self):

        weather = self.get_weather()

        if weather is None:

            return {
                "unit": "C",
                "temperature": None
            }

        return {

            "unit": "C",

            "temperature":
                weather.get(
                    "temperature"
                )
        }

    # ==================================================
    # PUBLISH WEATHER
    # ==================================================

    def publish_weather(self):

        weather = self.get_weather()

        if weather is None:

            print(
                "WEATHER DATA NOT AVAILABLE"
            )

            return False

        data = {

            "weather":
                weather,

            "device":
                self.device_name
        }

        message = json.dumps(
            data
        )

        print("")
        print("WEATHER MESSAGE:")
        print(message)

        return self.publish(
            message
        )

    # ==================================================
    # PUBLISH TEMPERATURE
    # ==================================================

    def publish_temperature(self):

        temperature = self.get_temperature()

        data = {

            "temperature":
                temperature,

            "device":
                self.device_name
        }

        message = json.dumps(
            data
        )

        print("")
        print("TEMPERATURE MESSAGE:")
        print(message)

        return self.publish(
            message
        )