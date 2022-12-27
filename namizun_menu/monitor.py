from prettytable import PrettyTable
from psutil import cpu_percent
from namizun_core import database, network
from namizun_menu import display
from time import sleep


def total_upload_color(total_upload, total_download):
    value = max(0, (database.get_parameter('coefficient_limitation') - total_upload / (total_download + 1))) / \
            database.get_parameter('coefficient_limitation') * 100
    if 66 <= value <= 100:
        return display.red_color + network.get_size(total_upload) + display.cornsilk_color
    elif 33 <= value < 66:
        return display.yellow_color + network.get_size(total_upload) + display.cornsilk_color
    else:
        return display.green_color + network.get_size(total_upload) + display.cornsilk_color


def total_download_color(total_download):
    if total_download < 700000000000:
        return display.green_color + network.get_size(total_download) + display.cornsilk_color
    elif 700000000000 <= total_download < 1500000000000:
        return display.yellow_color + network.get_size(total_download) + display.cornsilk_color
    else:
        return display.red_color + network.get_size(total_download) + display.cornsilk_color


def upload_speed_color(upload_speed):
    if 0 <= upload_speed < 8000000:
        return display.green_color + network.get_size(upload_speed) + display.cornsilk_color
    elif 8000000 <= upload_speed < 15000000:
        return display.yellow_color + network.get_size(upload_speed) + display.cornsilk_color
    else:
        return display.red_color + network.get_size(upload_speed) + display.cornsilk_color


def download_speed_color(download_speed):
    if 0 <= download_speed < 2000000:
        return display.green_color + network.get_size(download_speed) + display.cornsilk_color
    elif 2000000 <= download_speed < 5000000:
        return display.yellow_color + network.get_size(download_speed) + display.cornsilk_color
    else:
        return display.red_color + network.get_size(download_speed) + display.cornsilk_color


def cpu_percent_color(cpu_usage_percent):
    if 0 <= cpu_usage_percent < 34:
        return display.green_color + str(cpu_usage_percent) + display.cornsilk_color
    elif 34 <= cpu_usage_percent < 66:
        return display.yellow_color + str(cpu_usage_percent) + display.cornsilk_color
    else:
        return display.red_color + str(cpu_usage_percent) + display.cornsilk_color


def system_usage():
    sleep(0.2)
    display.line_jumper(-15)
    display.line_remover(5)
    old_bytes_sent, old_bytes_recv = network.get_network_io()
    namizun_monitor = PrettyTable()
    namizun_monitor.field_names = [f"{display.cyan_color}Σ Upload{display.cornsilk_color}",
                                   f"{display.cyan_color}Σ Download{display.cornsilk_color}",
                                   f"{display.cyan_color}⇧ Speed{display.cornsilk_color}",
                                   f"{display.cyan_color}⇩ Speed{display.cornsilk_color}",
                                   f"{display.cyan_color}% CPU{display.cornsilk_color}"]
    namizun_monitor.add_row([0, 0, 0, 0, 0])
    print(f"{display.gold_color}---------------{display.magenta_color}MONITORING{display.gold_color}--------------\n\n"
          f"{display.cornsilk_color} {namizun_monitor}")
    display.line_jumper(+11)
    while True:
        sleep(1)
        if database.get_parameter('in_submenu') is None:
            display.clear_terminal()
            return exit()
        if database.get_parameter('in_submenu') is False:
            display.line_jumper(-15)
            display.line_remover(5)
            print(
                f"{display.gold_color}---------------{display.magenta_color}MONITORING"
                f"{display.gold_color}--------------\n{display.cornsilk_color}")
            new_bytes_sent, new_bytes_recv = network.get_network_io()
            namizun_monitor.add_row([
                total_upload_color(new_bytes_sent, new_bytes_recv),
                total_download_color(new_bytes_recv),
                upload_speed_color(new_bytes_sent - old_bytes_sent),
                download_speed_color(new_bytes_recv - old_bytes_recv),
                cpu_percent_color(cpu_percent())])
            namizun_monitor.del_row(0)
            print(namizun_monitor)
            display.line_jumper(+11)
            old_bytes_sent, old_bytes_recv = new_bytes_sent, new_bytes_recv


def network_usage_details_table():
    bytes_sent, bytes_recv = network.get_system_network_io()
    usage_table = PrettyTable()
    usage_table.field_names = [f"{display.cyan_color}{display.cornsilk_color}",
                               f"{display.cyan_color}Upload{display.cornsilk_color}",
                               f"{display.cyan_color}Download{display.cornsilk_color}"]
    usage_table.add_row([f"{display.cyan_color}system{display.cornsilk_color}",
                         network.get_size(bytes_sent),
                         network.get_size(bytes_recv)])
    upload_amount_synchronizer = database.get_parameter('upload_amount_synchronizer')
    download_amount_synchronizer = database.get_parameter('download_amount_synchronizer')
    usage_table.add_row([f"{display.cyan_color}synchronizer{display.cornsilk_color}",
                         network.get_size(upload_amount_synchronizer),
                         network.get_size(download_amount_synchronizer)])
    usage_table.add_row(['------------', '------------', '------------'])
    usage_table.add_row([f"{display.cyan_color}total{display.cornsilk_color}",
                         total_upload_color(bytes_sent + upload_amount_synchronizer,
                                            bytes_recv + download_amount_synchronizer),
                         total_download_color(bytes_recv + download_amount_synchronizer)])
    usage_table.add_row(['------------', '------------', '------------'])
    usage_table.add_row(['------------', '------------', '------------'])
    usage_table.add_row([f"{display.cyan_color}last cached{display.cornsilk_color}",
                         network.get_size(database.get_parameter('total_upload_cache')),
                         network.get_size(database.get_parameter('total_download_cache'))])
    print(
        f"{display.gold_color}------------{display.magenta_color}network usage details"
        f"{display.gold_color}------------\n\n{display.cornsilk_color}{usage_table}\n"
    )
