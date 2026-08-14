from modem import EC200U


def main():

    modem = EC200U()

    print("=" * 50)
    print("EC200U AT COMMAND TERMINAL")
    print("=" * 50)

    # Initialize modem
    if not modem.initialize():

        print("Modem initialization failed.")
        return

    print()
    print("Available commands:")
    print("  modem   - Modem information")
    print("  signal  - Signal information")
    print("  sim     - SIM status")
    print("  network - Network registration")
    print("  nwinfo  - LTE network information")
    print("  EXIT    - Exit terminal")
    print()
    print("You can also enter any AT command.")
    print("=" * 50)

    while True:

        try:

            command = input("AT> ")

            command = command.strip()

            if not command:
                continue

            # Exit
            if command.upper() == "EXIT":

                print("Exiting terminal...")
                break

            # Modem information
            elif command.lower() == "modem":

                response, status = modem.get_modem_info()

                print(response)
                print("STATUS:", status)

            # Signal information
            elif command.lower() == "signal":

                signal, status = modem.get_signal()

                if status == "OK" and signal is not None:

                    print("Signal Information")
                    print("-------------------")
                    print("RSSI:", signal["rssi"])
                    print("BER :", signal["ber"])
                    print("STATUS:", status)

                else:

                    print("Signal read failed.")
                    print("STATUS:", status)

            # SIM status
            elif command.lower() == "sim":

                sim, status = modem.get_sim_status()

                if status == "OK" and sim is not None:

                    print("SIM Status")
                    print("----------")
                    print("Status :", sim["status"])
                    print("Result :", sim["description"])
                    print("STATUS :", status)

                else:

                    print("SIM status read failed.")
                    print("STATUS:", status)

            # Network registration
            elif command.lower() == "network":

                network, status = modem.get_network_status()

                if status == "OK" and network is not None:

                    print("Network Registration")
                    print("--------------------")
                    print("Mode   :", network["n"])
                    print("Status :", network["stat"])
                    print("Result :", network["description"])
                    print("STATUS :", status)

                else:

                    print("Network status read failed.")
                    print("STATUS:", status)

            # Network information
            elif command.lower() == "nwinfo":

                network_info, status = modem.get_network_info()

                if status == "OK" and network_info is not None:

                    print("Network Information")
                    print("-------------------")
                    print("Technology :", network_info["technology"])
                    print("Operator   :", network_info["operator"])
                    print("Band       :", network_info["band"])
                    print("Channel    :", network_info["channel"])
                    print("STATUS     :", status)

                else:

                    print("Network information read failed.")
                    print("STATUS:", status)

            # Normal AT command
            else:

                response, status = modem.send_command(command)

                print(response)
                print("STATUS:", status)

            print()

        except KeyboardInterrupt:

            print()
            print("Terminal stopped.")
            break


main()