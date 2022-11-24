import redis

parameters = [
    'running', 'speed', 'coefficient', 'total_upload_before_reboot', 'total_download_before_reboot', 'in_submenu']
namizun_db = None
prefix = 'namizun_'

cache_parameters = {}


def singleton():
    global namizun_db
    if namizun_db is None:
        namizun_db = redis.Redis()
    return namizun_db


def get_default(key):
    if key == 'running':
        return True
    elif key == 'speed':
        return 3
    elif key == 'coefficient':
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
    else:
        return int(value)


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
