from prettytable import PrettyTable
from psutil import net_io_counters, cpu_percent
from namizun_core import display, database
from time import sleep


def get_size(only_bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if only_bytes < 1024:
            return f"{only_bytes:.2f}{unit}B"
        only_bytes /= 1024


def get_network_io():
    io = net_io_counters()
    return io.bytes_sent + database.get_parameter('total_upload_before_reboot') \
        , io.bytes_recv + database.get_parameter('total_download_before_reboot')


def total_upload_color(total_upload, total_download):
    value = max(0, (database.get_parameter('coefficient_limitation') - total_upload / total_download)) / \
            database.get_parameter('coefficient_limitation') * 100
    if 66 <= value <= 100:
        return display.red + get_size(total_upload) + display.cornsilk
    elif 33 <= value < 66:
        return display.yellow + get_size(total_upload) + display.cornsilk
    else:
        return display.green + get_size(total_upload) + display.cornsilk


def total_download_color(total_download):
    if 0 <= total_download < 700000000000:
        return display.green + get_size(total_download) + display.cornsilk
    elif 700000000000 <= total_download < 1500000000000:
        return display.yellow + get_size(total_download) + display.cornsilk
    else:
        return display.red + get_size(total_download) + display.cornsilk


def upload_speed_color(upload_speed):
    if 0 <= upload_speed < 8000000:
        return display.green + get_size(upload_speed) + display.cornsilk
    elif 8000000 <= upload_speed < 15000000:
        return display.yellow + get_size(upload_speed) + display.cornsilk
    else:
        return display.red + get_size(upload_speed) + display.cornsilk


def download_speed_color(download_speed):
    if 0 <= download_speed < 2000000:
        return display.green + get_size(download_speed) + display.cornsilk
    elif 2000000 <= download_speed < 5000000:
        return display.yellow + get_size(download_speed) + display.cornsilk
    else:
        return display.red + get_size(download_speed) + display.cornsilk


def cpu_percent_color(cpu_usage_percent):
    if 0 <= cpu_usage_percent < 34:
        return display.green + str(cpu_usage_percent) + display.cornsilk
    elif 34 <= cpu_usage_percent < 66:
        return display.yellow + str(cpu_usage_percent) + display.cornsilk
    else:
        return display.red + str(cpu_usage_percent) + display.cornsilk


def monitor():
    sleep(0.2)
    display.line_jumper(-21)
    display.line_remover(5)
    old_bytes_sent, old_bytes_recv = get_network_io()
    namizun_monitor = PrettyTable()
    namizun_monitor.field_names = [f"{display.cyan}Σ Upload{display.cornsilk}",
                                   f"{display.cyan}Σ Download{display.cornsilk}",
                                   f"{display.cyan}⇧ Speed{display.cornsilk}",
                                   f"{display.cyan}⇩ Speed{display.cornsilk}",
                                   f"{display.cyan}% CPU{display.cornsilk}"]
    namizun_monitor.add_row([0, 0, 0, 0, 0])
    print(f"{display.gold}---------------{display.magenta}MONITORING{display.gold}--------------\n\n{display.cornsilk}"
          f"{namizun_monitor}")
    display.line_jumper(+17)
    while True:
        sleep(1)
        if database.get_parameter('in_submenu') is None:
            display.clear()
            return exit()
        if database.get_parameter('in_submenu') is False:
            display.line_jumper(-21)
            display.line_remover(5)
            print(
                f"{display.gold}---------------{display.magenta}MONITORING{display.gold}--------------\n{display.cornsilk}")
            new_bytes_sent, new_bytes_recv = get_network_io()
            namizun_monitor.add_row([
                total_upload_color(new_bytes_sent, new_bytes_recv),
                total_download_color(new_bytes_recv),
                upload_speed_color(new_bytes_sent - old_bytes_sent),
                download_speed_color(new_bytes_recv - old_bytes_recv),
                cpu_percent_color(cpu_percent())])
            namizun_monitor.del_row(0)
            print(namizun_monitor)
            display.line_jumper(+17)
            old_bytes_sent, old_bytes_recv = new_bytes_sent, new_bytes_recv
