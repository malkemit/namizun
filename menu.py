from namizun_core import display, database
from namizun_core.monitor import get_size
from threading import Thread
from namizun_core.monitor import monitor
from os import system, path


def fake_udp__uploader_running_setter():
    display.banner()
    print(f"\n{display.cornsilk}Do you want fake udp uploader to be activated?\n")
    selection = input(f"\n{display.green}y{display.cornsilk}/{display.red}n{display.cornsilk}?\n")
    if selection.lower() == 'y':
        database.set_parameter('fake_udp_uploader_running', True)
        return main_menu()
    elif selection.lower() == 'n':
        database.set_parameter('fake_udp_uploader_running', False)
        return main_menu()
    else:
        return fake_udp__uploader_running_setter()


def coefficient_of_buffer_size_setter():
    display.banner()
    print(f"\n{display.cornsilk}Choose coefficient of buffer size? (max = 6, min = 1)\n\n"
          f"{display.red}Warning: The larger the buffer size, the more likely the provider will notice that "
          f"your traffic is fake, BE CAREFUL!{display.cornsilk}\n")
    selection = int(input(f"\n{display.cyan}1{display.cornsilk} to {display.cyan}5{display.cornsilk}?"))
    if selection in range(1, 7):
        database.set_parameter('coefficient_buffer_size', selection)
        return main_menu()
    else:
        return coefficient_of_buffer_size_setter()


def coefficient_uploader_threads_count_setter():
    display.banner()
    print(f"\n{display.cornsilk}Choose coefficient of uploader threads count? (max = 30, min = 1)\n\n"
          f"{display.red}Warning: The higher the speed, the higher the CPU consumption!{display.cornsilk}\n")
    selection = int(input(f"\n{display.cyan}1{display.cornsilk} to {display.cyan}30{display.cornsilk}?"))
    if selection in range(1, 31):
        database.set_parameter('coefficient_uploader_threads_count', selection)
        return main_menu()
    else:
        return coefficient_uploader_threads_count_setter()


def coefficient_of_limitation_setter():
    display.banner()
    print(f"\n{display.cornsilk}What is your limit coefficient?"
          f"(max = {display.cyan}15{display.cornsilk}, min = {display.cyan}3{display.cornsilk})\n\n"
          f"For example, if you need to observe the ratio of {display.cyan}1{display.cornsilk} to "
          f"{display.cyan}10{display.cornsilk}, enter the value of {display.cyan}10{display.cornsilk}")
    selection = int(input(f"\n{display.cyan}3{display.cornsilk} to {display.cyan}15{display.cornsilk}?"))
    if selection in range(3, 16):
        database.set_parameter('coefficient_limitation', selection)
        return main_menu()
    else:
        return coefficient_of_limitation_setter()


def total_upload_before_reboot_setter():
    display.banner()
    print(f"\n{display.cornsilk}How much did you upload before the last reboot?"
          f"(max = {display.cyan}1000000{display.cornsilk}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    if selection <= 1000000:
        database.set_parameter('total_upload_before_reboot', selection * 1024 * 1024 * 1024)
        return main_menu()
    else:
        return total_upload_before_reboot_setter()


def total_download_before_reboot_setter():
    display.banner()
    print(f"\n{display.cornsilk}How much did you download before the last reboot?"
          f"(max = {display.cyan}100000{display.cornsilk}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    if selection <= 100000:
        database.set_parameter('total_download_before_reboot', selection * 1024 * 1024 * 1024)
        return main_menu()
    else:
        return total_download_before_reboot_setter()


def reload_namizun_service():
    if path.isfile('/var/www/namizun/range_ips'):
        database.set_parameter('range_ips', open('/var/www/namizun/range_ips').read())
    else:
        system('cp /var/www/namizun/else/range_ips /var/www/namizun/range_ips')
        database.set_parameter('range_ips', open('/var/www/namizun/range_ips').read())
    system('systemctl restart namizun.service')


def fake_udp_uploader_running_status():
    if database.get_parameter('fake_udp_uploader_running'):
        return display.green + "True"
    else:
        return display.red + "False"


def speedtest_uploader_running_status():
    if database.get_parameter('speedtest_uploader_running'):
        return display.green + "True"
    else:
        return display.red + "False"


def main_menu():
    display.banner()
    database.set_parameter('in_submenu', False)
    print(
        f"\n\n\n\n\n\n\n"
        f"{display.gold}--------------{display.magenta}Control menu{display.gold}-------------\n\n{display.cornsilk}"
        f"[1] - Fake udp uploader running : "
        f"{fake_udp_uploader_running_status() + display.cornsilk}\n"
        f"[2] - Speedtest uploader running : "
        f"{speedtest_uploader_running_status() + display.cornsilk} (coming soon)\n\n"
        f"[3] - Coefficient of buffer size : "
        f"{display.cyan + str(database.get_parameter('coefficient_buffer_size')) + display.cornsilk}\n"
        f"[4] - Coefficient of uploader threads count : "
        f"{display.cyan + str(database.get_parameter('coefficient_uploader_threads_count')) + display.cornsilk}\n"
        f"[5] - Coefficient of upload/download : "
        f"{display.cyan + str(database.get_parameter('coefficient_limitation')) + display.cornsilk}\n\n"
        f"[6] - Total Upload Before Reboot : "
        f"{display.cyan + str(get_size(database.get_parameter('total_upload_before_reboot'))) + display.cornsilk}\n"
        f"[7] - Total Download Before Reboot : "
        f"{display.cyan + str(get_size(database.get_parameter('total_download_before_reboot'))) + display.cornsilk}\n\n"
        f"[9] - Reload\n"
        f"[0] - Exit\n\n"
        f"ENTER YOUR SELECTION: \n\n")
    display.description()
    display.line_jumper(-9)
    user_choice = input()
    if user_choice == '1':
        database.set_parameter('in_submenu', True)
        return fake_udp__uploader_running_setter()
    elif user_choice == '3':
        database.set_parameter('in_submenu', True)
        return coefficient_of_buffer_size_setter()
    elif user_choice == '4':
        database.set_parameter('in_submenu', True)
        return coefficient_uploader_threads_count_setter()
    elif user_choice == '5':
        database.set_parameter('in_submenu', True)
        return coefficient_of_limitation_setter()
    elif user_choice == '6':
        database.set_parameter('in_submenu', True)
        return total_upload_before_reboot_setter()
    elif user_choice == '7':
        database.set_parameter('in_submenu', True)
        return total_download_before_reboot_setter()
    elif user_choice == '9':
        reload_namizun_service()
        return main_menu()
    elif user_choice == '0':
        database.set_parameter('in_submenu', None)
        print(display.reset)
        return exit()
    else:
        return main_menu()


Thread(target=monitor).start()
Thread(target=main_menu).start()
