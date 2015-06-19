import time


def get_today_string():
    localtime = time.localtime()
    today = time.strftime("%Y-%m-%d", localtime)
    return today


def get_now_string():
    localtime = time.localtime()
    today = time.strftime("%H:%M:%S", localtime)
    return today
