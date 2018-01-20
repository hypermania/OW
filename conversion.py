"""
Convert parsed career profile dict accessable data.
"""
from os import listdir
import re
import time
import json

from parsing import parse_career_profile
from util import convert_time, compute_time


def process_time_dict(play_time: dict):
    max_num = 0
    max_hour = 0
    for time in play_time.values():
        desc = time[0]
        frac = float(time[1])
        if desc == '--':
            continue
        parts = desc.split(' ')
        num = float(parts[0])
        unit = parts[1]
        if num > max_num:
            max_num = num
            if unit == 'hours' or unit == 'hour':
                max_hour = num / frac
            if unit == 'minutes' or unit == 'minute':
                max_hour = (num / 60.0) / frac
            if unit == 'seconds' or unit == 'second':
                max_hour = (num / 3600.0) / frac
                
    for hero in play_time.keys():
        play_time[hero] = max_hour * float(play_time[hero][1])

def process_int_dict(int_stat: dict):
    for key in int_stat.keys():
        int_stat[key] = int(int_stat[key][0].replace(',',''))
        
def process_float_dict(float_stat: dict):
    for key in float_stat.keys():
        float_stat[key] = float(float_stat[key][0])

def process_percentage_dict(percentage_stat: dict):
    for key in percentage_stat.keys():
        percentage_stat[key] = int(percentage_stat[key][0][:-1]) / 100.0

def format_stat(stat: str):
    stat = stat.replace(',', '')

    if stat == '--':
        return 0
    
    if stat[-1] == '%':
        return int(stat[:-1]) / 100.0
    
    int_match = re.fullmatch('\d+', stat)
    if int_match is not None:
        return int(stat)

    float_match = re.fullmatch('(\S+)\.(\S+)', stat)
    if float_match is not None:
        return float(stat)
    
    time_match = re.fullmatch('(\d+):(\d+)', stat)
    if time_match is not None:
        minute = int(time_match.group(1))
        second = int(time_match.group(2))
        return minute / 60.0 + second / 3600.0

    time_match = re.fullmatch('(\d+):(\d+):(\d+)', stat)
    if time_match is not None:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        second = int(time_match.group(3))
        return hour + minute / 60.0 + second / 3600.0

    time_match = re.fullmatch('(\d+) (\S+)', stat)
    if time_match is not None:
        return compute_time(time_match.group(1), time_match.group(2))
    
    time_match = re.fullmatch('(\d+\.\d+) (\S+)', stat)
    if time_match is not None:
        return compute_time(time_match.group(1), time_match.group(2))

    print("stat = {}".format(stat))
    raise Exception("Something unknown!")
    return None


def convert_parsed(parsed: dict) -> dict:
    
    if parsed == None:
        return None
    
    """
    Convert general info.
    """
    rank_str = parsed['general_info']['rank']
    if rank_str != None:
        parsed['general_info']['rank'] = int(rank_str)


    """
    Convert stats.
    """
    def convert_game_mode(mode: dict) -> dict:
        """
        Convert general stats.
        """
        general_stats = mode['general_stats']
        for stat in general_stats:
            if stat == 'Time Played':
                process_time_dict(general_stats[stat])
            if stat == 'Games Won':
                process_int_dict(general_stats[stat])
            if stat == 'Win Percentage':
                process_percentage_dict(general_stats[stat])
            if stat == 'Weapon Accuracy':
                process_percentage_dict(general_stats[stat])
            if stat == 'Eliminations per Life':
                process_float_dict(general_stats[stat])
            if stat == 'Multikill - Best':
                process_int_dict(general_stats[stat])
            if stat == 'Objective Kills - Average':
                process_float_dict(general_stats[stat])

        def format_dict(stats: dict):
            for sub_elem in stats.keys():
                if isinstance(stats[sub_elem], dict):
                    format_dict(stats[sub_elem])
                else:
                    stats[sub_elem] = format_stat(stats[sub_elem])
                
        hero_stats = mode['hero_stats']
        format_dict(hero_stats)
                
    convert_game_mode(parsed['quickplay_stats'])
    convert_game_mode(parsed['competitive_stats'])
        


samples = []

sample_filenames = listdir('./sample/')
for filename in sample_filenames:
    f = open('./sample/' + filename, 'r')
    samples.append(f.read())
    f.close()

print(time.strftime('%X') + (": Begin parsing."))
all_parsed = []
for sample in samples:
    all_parsed.append(parse_career_profile(sample))
print(time.strftime('%X') + (": End parsing."))

print(time.strftime('%X') + (": Begin conversion."))
for parsed in all_parsed:
    convert_parsed(parsed)
print(time.strftime('%X') + (": End conversion."))


"""          
print(time.strftime('%X') + (": Begin dumps."))
for parsed in all_parsed:
    json.dumps(parsed)
print(time.strftime('%X') + (": End dumps."))


save_file = open('./data/dumps.json', 'w')
for parsed in all_parsed:
    save_file.write("{}\n".format(json.dumps(parsed)))
"""


props = []
ranks = []
for parsed in all_parsed:
    s = sum(parsed['competitive_stats']['general_stats']['Time Played'].values())
    if s != 0 and parsed['general_info']['rank'] is not None:
        p = parsed['competitive_stats']['general_stats']['Time Played']['Mccree'] / s
        props.append(p)
        ranks.append(parsed['general_info']['rank'])
