import re

def convert_time(time: str):
    if time == '--':
        return 0
    parts = time.split(' ')
    num = parts[0]
    unit = parts[1]
    if unit == 'hours' or unit == 'hour':
        return float(num) 
    if unit == 'minutes' or unit == 'minute':
        return float(num) / 60.0
    if unit == 'seconds' or unit == 'second':
        return float(num) / 3600.0

def compute_time(num: str, unit: str):
    if unit == 'hours' or unit == 'hour':
        return float(num) 
    if unit == 'minutes' or unit == 'minute':
        return float(num) / 60.0
    if unit == 'seconds' or unit == 'second':
        return float(num) / 3600.0


def check_name(name: str):
    l = len(name)
    return l >= 3 and l <= 12
