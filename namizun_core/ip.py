from namizun_core import database
from random import choice, randint

cache_ip_list = {}


def get_random_range_ip_from_database():
    return choice(database.get_cache_parameter('range_ips').split('\n'))


def get_random_ip_from_database():
    fragmented_random_ip = get_random_range_ip_from_database().split('.')
    if fragmented_random_ip[0].isdigit() and 0 < int(fragmented_random_ip[0]) < 255 and \
            fragmented_random_ip[1].isdigit() and 0 < int(fragmented_random_ip[1]) < 255 and \
            fragmented_random_ip[2].isdigit() and 0 <= int(fragmented_random_ip[2]) < 255 and \
            fragmented_random_ip[3].isdigit() and 0 <= int(fragmented_random_ip[3]) < 255:
        return f"{fragmented_random_ip[0]}.{fragmented_random_ip[1]}." \
               f"{fragmented_random_ip[2] if int(fragmented_random_ip[2]) != 0 else randint(1, 255)}." \
               f"{fragmented_random_ip[3] if int(fragmented_random_ip[3]) != 0 else randint(1, 255)}"
    else:
        return get_random_ip_from_database()


def get_game_port():
    return choice([3478, 28960, 27014, 27020, 25565, 27015, 3724, 5000])


def cache_ip_ports_from_database():
    global cache_ip_list
    cache_ip_list = database.get_ip_ports_from_database()


def get_random_ip_port():
    if len(cache_ip_list) > 0:
        target_ip, target_port = choice(list(cache_ip_list.items()))
        del cache_ip_list[target_ip]
    else:
        target_ip = get_random_ip_from_database()
        target_port = get_game_port()
        database.set_ip_port_to_database(target_ip, target_port)
    return target_ip, target_port
