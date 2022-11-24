from namizun_core import ip, database
from random import choice
from threading import Thread
from random import randint
from time import sleep
import socket


def get_random_ip():
    return choice(ip.ips) + str(randint(1, 255))


def start_udp_uploader(udp_upload_size, target_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while udp_upload_size >= 0:
        buf = int(randint(3000, 6000) * database.get_cache_parameter('speed') * 4 / 5)
        if sock.sendto(bytes(buf), (target_ip, 443)):
            udp_upload_size -= buf
            sleep(0.01)
    sock.close()


def multi_udp_uploader(udp_upload_size):
    udp_thread_count = int(randint(3, 7) * database.get_cache_parameter('speed') * 3 / 4)
    threads = []
    for sender_agent in range(udp_thread_count):
        agent = Thread(target=start_udp_uploader, args=(udp_upload_size, get_random_ip()))
        agent.start()
        threads.append(agent)
    for sender_agent in threads:
        sender_agent.join()
    sleep(randint(1, 5))
    return udp_thread_count
