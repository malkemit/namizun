from redis import Redis
from os import system, path
from random import choice

parameters = [
    'range_ips', 'fake_udp_uploader_running', 'speedtest_uploader_running',
    'coefficient_buffer_size', 'coefficient_uploader_threads_count', 'coefficient_limitation',
    'total_upload_before_reboot', 'total_download_before_reboot', 'in_submenu']
namizun_db = None
prefix = 'namizun_'
cache_parameters = {}


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
            system('ln -s /var/www/namizun/else/range_ips /var/www/namizun/')
            return open('/var/www/namizun/range_ips').read()
    elif key == 'fake_udp_uploader_running':
        return True
    elif key == 'speedtest_uploader_running':
        return False
    elif key == 'coefficient_buffer_size':
        return 2
    elif key == 'coefficient_uploader_threads_count':
        return 5
    elif key == 'coefficient_limitation':
        return 10
    elif key == 'total_upload_before_reboot':
        return 0
    elif key == 'total_download_before_reboot':
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
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
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


def set_parameters_to_cache():
    for key in parameters:
        cache_parameters[key] = get_parameter(key)


def get_random_range_ip():
    return choice(get_cache_parameter('range_ips').split('\n'))
