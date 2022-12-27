from namizun_core import database
from namizun_menu import udp_submenu, display, network_submenu
from namizun_core.network import get_size
from os import system, path


def reload_namizun_service():
    if path.isfile('/var/www/namizun/range_ips'):
        database.set_parameter('range_ips', open('/var/www/namizun/range_ips').read())
    else:
        system('cp /var/www/namizun/else/range_ips /var/www/namizun/range_ips')
        database.set_parameter('range_ips', open('/var/www/namizun/range_ips').read())
    system('systemctl restart namizun.service')


def menu():
    display.banner()
    database.set_parameter('in_submenu', False)
    print(
        f"\n\n\n\n\n\n\n"
        f"{display.gold_color}--------------{display.magenta_color}Control menu{display.gold_color}-------------\n\n"
        f"{display.cornsilk_color}[1] - Fake udp uploader menu : "

        f"settings: {udp_submenu.fake_udp_uploader_running_status() + display.cornsilk_color} / "
        f"{display.cyan_color + str(database.get_parameter('coefficient_buffer_size')) + display.cornsilk_color} / "
        f"{display.cyan_color + str(database.get_parameter('coefficient_uploader_threads_count'))}"
        f"{display.cornsilk_color} / {display.cyan_color}"
        f"{str(database.get_parameter('coefficient_buffer_sending_speed')) + display.cornsilk_color}\n\n"
        f"[2] - network menu : "
        f"(Σ Upload= "
        f"{display.cyan_color + str(get_size(database.get_parameter('total_upload_cache'))) + display.cornsilk_color} "
        f"|| Σ Download= "
        f"{display.cyan_color + str(get_size(database.get_parameter('total_download_cache'))) + display.cornsilk_color}"
        f")\n\n"
        f"{display.cornsilk_color}[9] - Reload\n"
        f"[0] - Exit\n\n"
        f"ENTER YOUR SELECTION: \n")
    user_choice = input()
    if user_choice == '1':
        database.set_parameter('in_submenu', True)
        return udp_submenu.menu()
    elif user_choice == '2':
        database.set_parameter('in_submenu', True)
        return network_submenu.menu()
    elif user_choice == '9':
        reload_namizun_service()
        return menu()
    elif user_choice == '0':
        database.set_parameter('in_submenu', None)
        print(display.reset_color)
        return exit()
    else:
        return menu()
