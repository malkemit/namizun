from datetime import datetime
from pytz import timezone


def get_now_date():
    return datetime.now(timezone('Asia/Tehran')).strftime('%d-%m-%Y')


def get_now_time():
    return datetime.now(timezone('Asia/Tehran')).strftime('%H:%M:%S')


def get_now_hour():
    return datetime.now(timezone('Asia/Tehran')).strftime('%H')
