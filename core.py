import config
from threading import Thread
from random import randint
import socket
from time import sleep
from monitor import get_network_io
from ip import ips
from random import choice


def get_network_usage():
    upload, download = get_network_io()
    difference = download - upload / randint(
        config.get_cache_parameter('coefficient') - 3, config.get_cache_parameter('coefficient') + 3)
    if difference < 1:
        return 1
    elif difference > 100000000 * config.get_cache_parameter('speed'):
        return 100000000 * config.get_cache_parameter('speed')
    return difference


def get_random_ip():
    return choice(ips) + str(randint(1, 255))


def start_udp_uploader(udp_upload_size, target_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while udp_upload_size >= 0:
        buf = int(randint(3000, 6000) * config.get_cache_parameter('speed') * 4 / 5)
        if sock.sendto(bytes(buf), (target_ip, 443)):
            udp_upload_size -= buf
            sleep(0.01)
    sock.close()


def multi_udp_uploader(udp_upload_size):
    udp_thread_count = int(randint(3, 7) * config.get_cache_parameter('speed') * 3 / 4)
    threads = []
    for sender_agent in range(udp_thread_count):
        agent = Thread(target=start_udp_uploader, args=(udp_upload_size, get_random_ip()))
        agent.start()
        threads.append(agent)
    for sender_agent in threads:
        sender_agent.join()
    sleep(randint(1, 5))
    return udp_thread_count


while True:
    config.set_parameters_to_cache()
    if config.get_cache_parameter('running'):
        count = randint(70, 140)
        size = get_network_usage()
        while count >= 0:
            count -= multi_udp_uploader(size)
    sleep(randint(50, 200))
