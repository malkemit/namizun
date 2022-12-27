from namizun_core import database
from namizun_menu import main_menu, display, monitor
from namizun_core.network import get_size, get_system_download, get_system_upload, get_system_network_io


def coefficient_of_limitation_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}What is your limit coefficient?"
          f"(max = {display.cyan_color}15{display.cornsilk_color}, min = {display.cyan_color}2"
          f"{display.cornsilk_color})\n\n"
          f"For example, if you need to observe the ratio of {display.cyan_color}1{display.cornsilk_color} to "
          f"{display.cyan_color}10{display.cornsilk_color}, enter the value of {display.cyan_color}10"
          f"{display.cornsilk_color}")
    selection = int(input(f"\n{display.cyan_color}2{display.cornsilk_color} to {display.cyan_color}15"
                          f"{display.cornsilk_color}?"))
    if selection in range(2, 16):
        database.set_parameter('coefficient_limitation', selection)
        return menu()
    else:
        return coefficient_of_limitation_setter()


def upload_amount_synchronizer_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Enter the upload synchronizer amount"
          f"(max = {display.cyan_color}1000000{display.cornsilk_color}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    system_upload = get_system_upload()
    if -1 * (system_upload / (1024 * 1024 * 1024)) <= selection <= 1000000:
        upload_amount_synchronizer = selection * 1024 * 1024 * 1024
        database.set_parameter('upload_amount_synchronizer', upload_amount_synchronizer)
        database.set_parameter('total_upload_cache', system_upload + upload_amount_synchronizer)
        return menu()
    else:
        return upload_amount_synchronizer_setter()


def download_amount_synchronizer_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Enter the download synchronizer amount"
          f"(max = {display.cyan_color}100000{display.cornsilk_color}GB)\n")
    selection = int(input("\nJust enter GB amount?"))
    system_download = get_system_download()
    if -1 * (system_download / (1024 * 1024 * 1024)) <= selection <= 100000:
        download_amount_synchronizer = selection * 1024 * 1024 * 1024
        database.set_parameter('download_amount_synchronizer', download_amount_synchronizer)
        database.set_parameter('total_download_cache', system_download + download_amount_synchronizer)
        return menu()
    else:
        return download_amount_synchronizer_setter()


def reset_network_usage():
    display.banner()
    print(f"\n{display.cornsilk_color}Are you sure to set the traffic to zero?\n")
    selection = input(f"\n{display.green_color}y{display.cornsilk_color}/{display.red_color}n"
                      f"{display.cornsilk_color}?\n")
    if selection.lower() == 'y':
        upload_size, download_size = get_system_network_io()
        database.set_parameter('download_amount_synchronizer', -1 * download_size)
        database.set_parameter('upload_amount_synchronizer', -1 * upload_size)
        database.set_parameter('total_download_cache', 0)
        database.set_parameter('total_upload_cache', 0)
        return menu()
    elif selection.lower() == 'n':
        return menu()
    else:
        return reset_network_usage()


def menu():
    display.banner()
    monitor.network_usage_details_table()
    print(
        f"{display.gold_color}--------------{display.magenta_color}network usage menu"
        f"{display.gold_color}-------------\n\n{display.cornsilk_color}"
        f"[1] - Coefficient of upload/download : "
        f"{display.cyan_color + str(database.get_parameter('coefficient_limitation')) + display.cornsilk_color}\n\n"
        f"[2] - Upload amount synchronizer : "
        f"{display.cyan_color + str(get_size(database.get_parameter('upload_amount_synchronizer')))}\n"
        f"{display.cornsilk_color}[3] - Download amount synchronizer : "
        f"{display.cyan_color + str(get_size(database.get_parameter('download_amount_synchronizer')))}\n\n"
        f"{display.cornsilk_color}[9] - RESET NETWORK USAGE\n"
        f"[0] - Back to main menu\n\n"
        f"ENTER YOUR SELECTION: \n\n")
    user_choice = input()
    if user_choice == '1':
        return coefficient_of_limitation_setter()
    elif user_choice == '2':
        return upload_amount_synchronizer_setter()
    elif user_choice == '3':
        return download_amount_synchronizer_setter()
    elif user_choice == '9':
        return reset_network_usage()
    elif user_choice == '0':
        return main_menu.menu()
    else:
        return menu()
