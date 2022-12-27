from redis import Redis
from os import system, path
from random import randint

parameters = [
    'fake_udp_uploader_running',
    'coefficient_buffer_size', 'coefficient_uploader_threads_count', 'coefficient_buffer_sending_speed',
    'range_ips', 'in_submenu', 'coefficient_limitation',
    'total_upload_cache', 'total_download_cache', 'download_amount_synchronizer', 'upload_amount_synchronizer']
namizun_db = None
prefix = 'namizun_'
ip_prefix = f'{prefix}ip_'
cache_parameters = {}
buffers_weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def singleton():
    global namizun_db
    if namizun_db is None:
        namizun_db = Redis()
    return namizun_db


def get_default(key):
    if key == 'range_ips':
        if path.isfile('/var/www/namizun/range_ips'):
            return open('/var/www/namizun/range_ips').read()
        else:
            system('cp /var/www/namizun/else/range_ips /var/www/namizun/')
            return open('/var/www/namizun/range_ips').read()
    elif key == 'fake_udp_uploader_running':
        return True
    elif key == 'coefficient_buffer_size':
        return 1
    elif key == 'coefficient_uploader_threads_count':
        return 3
    elif key == 'coefficient_buffer_sending_speed':
        return 1
    elif key == 'coefficient_limitation':
        return 6
    elif key == 'total_upload_cache':
        return 0
    elif key == 'total_download_cache':
        return 0
    elif key == 'upload_amount_synchronizer':
        return 0
    elif key == 'download_amount_synchronizer':
        return 0
    elif key == 'in_submenu':
        return False


def check_datatype(value):
    if isinstance(value, bytes):
        value = value.decode('UTF-8')
    if value == 'False':
        return False
    elif value == 'True':
        return True
    elif value == 'None':
        return None
    else:
        try:
            return int(value)
        except ValueError:
            return value


def get_parameter(key):
    if key in parameters:
        my_db = singleton()
        data = my_db.get(prefix + key)
        if data is None:
            data = get_default(key)
            my_db.set(prefix + key, str(data))
        return check_datatype(data)
    else:
        return None


def set_parameter(key, value):
    if key in parameters:
        singleton().set(prefix + key, str(value))
        return value
    else:
        return None


def get_cache_parameter(key):
    if key in parameters:
        return cache_parameters[key]
    else:
        return None


def get_buffers_weight():
    global buffers_weight
    selected_buffer_size = 2 * get_cache_parameter('coefficient_buffer_size') - 1
    buffers_weight = [
        1 / 2 ** abs(buffer_size - selected_buffer_size)
        for buffer_size in range(1, 14)
    ]


def set_parameters_to_cache():
    for key in parameters:
        cache_parameters[key] = get_parameter(key)
    get_buffers_weight()


def set_ip_port_to_database(target_ip, target_port):
    my_db = singleton()
    my_db.set(ip_prefix + target_ip, str(target_port), ex=randint(600, 6000))


def get_ip_ports_from_database():
    my_db = singleton()
    result = {}
    keys = my_db.keys(f"{ip_prefix}*")
    if len(keys) > 0:
        for key in keys:
            if isinstance(key, bytes):
                key = key.decode('UTF-8')
            ip = key.split('_')[-1]
            result[ip] = check_datatype(my_db.get(ip_prefix + ip))
    return result
