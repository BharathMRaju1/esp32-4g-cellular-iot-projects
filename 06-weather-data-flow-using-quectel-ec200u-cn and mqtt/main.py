from modem import EC200U


print("")
print("========================================")
print("       GRIDBox-4G MQTT APPLICATION")
print("========================================")


# ==========================================
# CREATE MODEM OBJECT
# ==========================================

modem = EC200U()


# ==========================================
# INITIALIZE EC200U
# ==========================================

modem.initialize()


# ==========================================
# ENSURE MQTT CONNECTION
# ==========================================

print("")
print("########################################")
print("#        STARTING MQTT")
print("########################################")

print("Broker:", modem.broker)
print("Port:", modem.port)
print("Username:", modem.username)
print("Topic:", modem.topic)


if modem.ensure_mqtt():

    print("")
    print("========================================")
    print("MQTT CONNECTION SUCCESSFUL")
    print("========================================")

else:

    print("")
    print("MQTT CONNECTION FAILED")

    print("")
    print("========================================")
    print("       PROGRAM COMPLETE")
    print("========================================")

    raise SystemExit


# ==========================================
# PUBLISH DEVICE STATUS
# ==========================================

print("")
print("########################################")
print("#       PUBLISHING DEVICE STATUS")
print("########################################")

modem.publish_device_status()


# ==========================================
# GET WEATHER
# ==========================================

print("")
print("########################################")
print("#          GETTING WEATHER")
print("########################################")

weather = modem.get_weather()


if weather is not None:

    print("")
    print("========================================")
    print("WEATHER SUCCESS")
    print("========================================")

    print(weather)

    # --------------------------------------
    # Publish weather
    # --------------------------------------

    weather_message = {
        "weather": weather,
        "device": modem.device_name
    }

    modem.publish(
        __import__("json").dumps(
            weather_message
        )
    )

else:

    print("")
    print("========================================")
    print("WEATHER DATA NOT AVAILABLE")
    print("========================================")


print("")
print("========================================")
print("       PROGRAM COMPLETE")
print("========================================")