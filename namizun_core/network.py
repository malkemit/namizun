from psutil import net_io_counters
from namizun_core import database


def get_size(only_bytes):
    flag = ''
    if only_bytes < 0:
        flag = '-'
        only_bytes *= -1
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if only_bytes < 1024:
            return f"{flag}{only_bytes:.2f}{unit}B"
        only_bytes /= 1024


def get_network_io():
    io = net_io_counters()
    return io.bytes_sent + database.get_parameter('upload_amount_synchronizer') \
        , io.bytes_recv + database.get_parameter('download_amount_synchronizer')


def get_system_network_io():
    io = net_io_counters()
    return io.bytes_sent, io.bytes_recv


def get_system_upload():
    return net_io_counters().bytes_sent


def get_system_download():
    return net_io_counters().bytes_recv
