import re

def convert_time(time: str):
    if time == '--':
        return None
    parts = time.split(' ')
    num = parts[0]
    unit = parts[1]
    if unit == 'hours' or unit == 'hour':
        return int(num) * 60 * 60
    if unit == 'minutes' or unit == 'minute':
        return int(num) * 60
    if unit == 'seconds' or unit == 'second':
        return int(num)

def check_name(name: str):
    l = len(name)
    return l >= 3 and l <= 12
