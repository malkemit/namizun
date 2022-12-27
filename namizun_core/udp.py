from namizun_core import database, ip
from threading import Thread
from random import uniform, randint
from time import sleep
from random import choices
import socket
from namizun_core.log import store_new_upload_agent_log, store_new_udp_uploader_log
from namizun_core.time import get_now_time

buffer_ranges = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000]
total_upload_size_for_each_ip = 0
uploader_count = 0


def start_udp_uploader():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_ip, game_port = ip.get_random_ip_port()
    remain_upload_size = upload_size = int(
        uniform(total_upload_size_for_each_ip * 0.7, total_upload_size_for_each_ip * 1.2))
    started_time = get_now_time()
    while remain_upload_size >= 0:
        selected_buffer_range = choices(buffer_ranges, database.buffers_weight, k=1)[0]
        buf = int(uniform(selected_buffer_range - 5000, selected_buffer_range))
        if sock.sendto(bytes(buf), (target_ip, game_port)):
            remain_upload_size -= buf
            sleep(0.001 * int(uniform(5, 26)) / database.get_cache_parameter('coefficient_buffer_sending_speed'))
    sock.close()
    store_new_udp_uploader_log(started_time, target_ip, game_port, upload_size, get_now_time())


def adjustment_of_upload_size_and_uploader_count(total_upload_size):
    global total_upload_size_for_each_ip, uploader_count
    uploader_count -= int(0.2 * uploader_count)
    total_upload_size_for_each_ip -= int(0.05 * total_upload_size_for_each_ip)
    if total_upload_size_for_each_ip * uploader_count > total_upload_size:
        adjustment_of_upload_size_and_uploader_count(total_upload_size)


def set_upload_size_and_uploader_count(total_upload_size, total_uploader_count):
    global total_upload_size_for_each_ip, uploader_count
    uploader_count = int(uniform(total_uploader_count * 0.05, total_uploader_count * 0.2))
    coefficient_of_upload = int((database.get_cache_parameter('coefficient_buffer_size') + 1) / 2)
    upload_size_max_range = choices([50, 100, 150], [1, 2, 3], k=1)[0]
    total_upload_size_for_each_ip = int(uniform((upload_size_max_range - 50) * coefficient_of_upload,
                                                upload_size_max_range * coefficient_of_upload)) * 1024 * 1024
    if total_upload_size_for_each_ip * uploader_count > total_upload_size:
        adjustment_of_upload_size_and_uploader_count(total_upload_size)


def multi_udp_uploader(total_upload_size, total_uploader_count):
    set_upload_size_and_uploader_count(total_upload_size, total_uploader_count)
    threads = []
    store_new_upload_agent_log(uploader_count, total_upload_size_for_each_ip)
    for sender_agent in range(uploader_count):
        agent = Thread(target=start_udp_uploader)
        agent.start()
        threads.append(agent)
    for sender_agent in threads:
        sender_agent.join()
    sleep(randint(1, 5))
    return uploader_count, total_upload_size_for_each_ip
