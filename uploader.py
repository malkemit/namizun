from namizun_core import database
from random import uniform, randint
from time import sleep
from namizun_core.network import get_network_io, get_system_network_io
from namizun_core.udp import multi_udp_uploader
from namizun_core.ip import cache_ip_ports_from_database
from namizun_core.time import get_now_hour
from namizun_core.log import store_restart_namizun_uploader_log, store_new_upload_loop_log


def reboot_finder():
    new_upload_amount, new_download_amount = get_network_io()
    cached_download_amount = database.get_cache_parameter('total_download_cache')
    cached_upload_amount = database.get_cache_parameter('total_upload_cache')
    if new_upload_amount >= cached_upload_amount and new_download_amount >= cached_download_amount:
        database.set_parameter('total_download_cache', new_download_amount)
        database.set_parameter('total_upload_cache', new_upload_amount)
    else:
        system_upload_amount, system_download_amount = get_system_network_io()
        database.set_parameter('download_amount_synchronizer', (cached_download_amount - system_download_amount))
        database.set_parameter('upload_amount_synchronizer', (cached_upload_amount - system_upload_amount))
        new_upload_amount = cached_upload_amount
        new_download_amount = cached_download_amount
    return new_upload_amount, new_download_amount


def get_network_usage():
    upload, download = reboot_finder()
    limitation = int(uniform(database.get_cache_parameter('coefficient_limitation') * 0.7,
                             database.get_cache_parameter('coefficient_limitation') * 1.3))
    difference = download * limitation - upload
    if difference < 1000000000:
        return 0
    return difference


def get_uploader_count_base_timeline():
    time_in_iran = int(get_now_hour())
    default_uploader_count = database.get_cache_parameter('coefficient_uploader_threads_count') * 10
    maximum_allowed_coefficient = [2, 1.6, 1, 0.6, 0.2, 0.1, 0.6, 1, 1.2, 1.3, 1.4, 1.5,
                                   1.3, 1.4, 1.6, 1.5, 1.3, 1.5, 1.7, 1.8, 2, 1.3, 1.5, 1.8]
    minimum_allowed_coefficient = [1.6, 1, 0.6, 0.2, 0, 0, 0.2, 0.8, 1, 1.1, 1.2, 1.3,
                                   1.1, 1.2, 1.5, 1.4, 1.2, 1.4, 1.5, 1.6, 1.8, 1, 1.2, 1.5]
    return int(uniform(minimum_allowed_coefficient[time_in_iran] * default_uploader_count,
                       maximum_allowed_coefficient[time_in_iran] * default_uploader_count))


store_restart_namizun_uploader_log()

while True:
    database.set_parameters_to_cache()
    if database.get_cache_parameter('fake_udp_uploader_running'):
        cache_ip_ports_from_database()
        total_upload_size = remain_upload_size = get_network_usage()
        total_uploader = remain_uploader = get_uploader_count_base_timeline()
        store_new_upload_loop_log(total_uploader, total_upload_size)
        while remain_uploader > 0 and remain_upload_size > 0.1 * total_upload_size:
            uploader_count, upload_size_for_each_ip = multi_udp_uploader(0.3 * total_upload_size, total_uploader)
            if uploader_count == 0:
                remain_uploader -= 1
            else:
                remain_uploader -= uploader_count
            remain_upload_size -= uploader_count * upload_size_for_each_ip
    sleep(randint(5, 30))
