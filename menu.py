from namizun_core import display, database
from time import sleep
from namizun_core.monitor import get_size
from threading import Thread
from namizun_core.monitor import monitor


def running_setter():
    display.banner()
    print(f"\n{display.cornsilk}Do you want uploader to be activated?")
    selection = input(f"\n{display.green}y{display.cornsilk}/{display.red}n{display.cornsilk}?\n")
    if selection.lower() == 'y':
        database.set_parameter('running', True)
        return main_menu()
    elif selection.lower() == 'n':
        database.set_parameter('running', False)
        return main_menu()
    else:
        return running_setter()


def speed_setter():
    display.banner()
    print(f"\n{display.cornsilk}Choose upload speed? (max = 5, min = 1)\n"
          f"{display.red}Warning: The higher the speed, the higher the CPU consumption{display.cornsilk}\n")
    selection = int(input(f"\n{display.cyan}1{display.cornsilk} to {display.cyan}5{display.cornsilk}?"))
    if selection in range(1, 6):
        database.set_parameter('speed', selection)
        return main_menu()
    else:
        return speed_setter()


def coefficient_setter():
    display.banner()
    print(f"\n{display.cornsilk}What is your limit coefficient?"
          f"(max = {display.cyan}12{display.cornsilk}, min = {display.cyan}3{display.cornsilk})\n")
    selection = int(input(f"\n{display.cyan}3{display.cornsilk} to {display.cyan}12{display.cornsilk}?"))
    if selection in range(1, 13):
        database.set_parameter('coefficient', selection)
        return main_menu()
    else:
        return coefficient_setter()


def total_upload_before_reboot_setter():
    display.banner()
    print(f"\n{display.cornsilk}How much did you upload before the last reboot?"
          f"(max = {display.cyan}50000{display.cornsilk}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    if selection <= 50000:
        database.set_parameter('total_upload_before_reboot', selection * 1024 * 1024 * 1024)
        return main_menu()
    else:
        return total_upload_before_reboot_setter()


def total_download_before_reboot_setter():
    display.banner()
    print(f"\n{display.cornsilk}How much did you download before the last reboot?"
          f"(max = {display.cyan}5000{display.cornsilk}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    if selection <= 5000:
        database.set_parameter('total_download_before_reboot', selection * 1024 * 1024 * 1024)
        return main_menu()
    else:
        return total_download_before_reboot_setter()


def running_status():
    if database.get_parameter('running'):
        return display.green + "True"
    else:
        return display.red + "False"


def main_menu():
    sleep(0.5)
    database.set_parameter('in_submenu', False)
    print(
        f"\n{display.gold}--------------{display.magenta}Control menu{display.gold}-------------\n\n{display.cornsilk}"
        f"[1] - Uploader Running : {running_status() + display.cornsilk}\n"
        f"[2] - Speed : {display.cyan + str(database.get_parameter('speed')) + display.cornsilk}\n"
        f"[3] - Coefficient : {display.cyan + str(database.get_parameter('coefficient')) + display.cornsilk}\n"
        f"[4] - Total Upload Before Reboot : "
        f"{display.cyan + str(get_size(database.get_parameter('total_upload_before_reboot'))) + display.cornsilk}\n"
        f"[5] - Total Download Before Reboot : "
        f"{display.cyan + str(get_size(database.get_parameter('total_download_before_reboot'))) + display.cornsilk}\n\n"
        f"[0] - Exit\n\n"
        f"ENTER YOUR SELECTION: \n\n")
    display.description()
    display.line_jumper(-9)
    user_choice = int(input())
    if user_choice == 1:
        database.set_parameter('in_submenu', True)
        return running_setter()
    elif user_choice == 2:
        database.set_parameter('in_submenu', True)
        return speed_setter()
    elif user_choice == 3:
        database.set_parameter('in_submenu', True)
        return coefficient_setter()
    elif user_choice == 4:
        database.set_parameter('in_submenu', True)
        return total_upload_before_reboot_setter()
    elif user_choice == 5:
        database.set_parameter('in_submenu', True)
        return total_download_before_reboot_setter()
    elif user_choice == 0:
        database.set_parameter('in_submenu', None)
        return print(display.reset) + exit()
    else:
        return main_menu()


Thread(target=monitor).start()
Thread(target=main_menu).start()
