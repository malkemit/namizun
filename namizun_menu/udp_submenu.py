from namizun_core import database
from namizun_menu import main_menu, display


def fake_udp_uploader_running_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Do you want fake udp uploader to be activated?\n")
    selection = input(f"\n{display.green_color}y{display.cornsilk_color}/{display.red_color}n"
                      f"{display.cornsilk_color}?\n")
    if selection.lower() == 'y':
        database.set_parameter('fake_udp_uploader_running', True)
        return menu()
    elif selection.lower() == 'n':
        database.set_parameter('fake_udp_uploader_running', False)
        return menu()
    else:
        return fake_udp_uploader_running_setter()


def coefficient_of_buffer_size_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Choose coefficient of buffer size? (max = 6, min = 1)\n\n"
          f"{display.red_color}Warning: The larger the buffer size, the more likely the provider will notice that "
          f"your traffic is fake, BE CAREFUL!{display.cornsilk_color}\n")
    selection = int(input(f"\n{display.cyan_color}1{display.cornsilk_color} to {display.cyan_color}6"
                          f"{display.cornsilk_color}?"))
    if selection in range(1, 7):
        database.set_parameter('coefficient_buffer_size', selection)
        return menu()
    else:
        return coefficient_of_buffer_size_setter()


def coefficient_uploader_threads_count_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Choose coefficient of uploader threads count? (max = 30, min = 1)\n\n"
          f"{display.red_color}Warning: The higher the speed, the higher the CPU consumption!"
          f"{display.cornsilk_color}\n")
    selection = int(input(f"\n{display.cyan_color}1{display.cornsilk_color} to {display.cyan_color}30"
                          f"{display.cornsilk_color}?"))
    if selection in range(1, 31):
        database.set_parameter('coefficient_uploader_threads_count', selection)
        return menu()
    else:
        return coefficient_uploader_threads_count_setter()


def coefficient_buffer_sending_speed_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Choose coefficient of buffer sending speed? (max = 5, min = 1)\n\n"
          f"{display.red_color}Warning: The higher the speed, the higher the CPU consumption!"
          f"{display.cornsilk_color}\n")
    selection = int(input(f"\n{display.cyan_color}1{display.cornsilk_color} to {display.cyan_color}5"
                          f"{display.cornsilk_color}?"))
    if selection in range(1, 6):
        database.set_parameter('coefficient_buffer_sending_speed', selection)
        return menu()
    else:
        return coefficient_uploader_threads_count_setter()


def fake_udp_uploader_running_status():
    if database.get_parameter('fake_udp_uploader_running'):
        return f"{display.green_color}True"
    else:
        return f"{display.red_color}False"


def menu():
    display.banner()
    print(
        f"{display.gold_color}--------------{display.magenta_color}Fake udp uploader menu"
        f"{display.gold_color}-------------\n\n{display.cornsilk_color}"
        f"[1] - Fake udp uploader running : "
        f"{fake_udp_uploader_running_status() + display.cornsilk_color}\n"
        f"[2] - Coefficient of buffer size : "
        f"{display.cyan_color + str(database.get_parameter('coefficient_buffer_size')) + display.cornsilk_color}\n"
        f"[3] - Coefficient of uploader threads count : "
        f"{display.cyan_color + str(database.get_parameter('coefficient_uploader_threads_count'))}\n"
        f"{display.cornsilk_color}[4] - Coefficient of buffer sending speed : "
        f"{display.cyan_color + str(database.get_parameter('coefficient_buffer_sending_speed'))}\n\n"
        f"{display.cornsilk_color}[0] - Back to main menu\n\n"
        f"ENTER YOUR SELECTION: \n\n")
    user_choice = input()
    if user_choice == '1':
        return fake_udp_uploader_running_setter()
    elif user_choice == '2':
        return coefficient_of_buffer_size_setter()
    elif user_choice == '3':
        return coefficient_uploader_threads_count_setter()
    elif user_choice == '4':
        return coefficient_buffer_sending_speed_setter()
    elif user_choice == '0':
        return main_menu.menu()
    else:
        return menu()
