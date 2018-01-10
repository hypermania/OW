import time
import re

from html5_parser import parse
from lxml import etree

hero_id = {
    "Reaper": "0x02E0000000000002",
    "Tracer": "0x02E0000000000003",
    "Mercy": "0x02E0000000000004",
    "Hanzo": "0x02E0000000000005",
    "Torbjorn": "0x02E0000000000006",
    "Reinhardt": "0x02E0000000000007",
    "Pharah": "0x02E0000000000008",
    "Winston": "0x02E0000000000009",
    "Widowmaker": "0x02E000000000000A",
    "Bastion": "0x02E0000000000015",
    "Symmetra": "0x02E0000000000016",
    "Zenyatta": "0x02E0000000000020",
    "Genji": "0x02E0000000000029",
    "Roadhog": "0x02E0000000000040",
    "Mccree": "0x02E0000000000042",
    "Junkrat": "0x02E0000000000065",
    "Zarya": "0x02E0000000000068",
    "Soldier:76": "0x02E000000000006E",
    "Lucio": "0x02E0000000000079",
    "Dva": "0x02E000000000007A",
    "Mei": "0x02E00000000000DD",
    "Ana": "0x02E000000000013B",
    "Sombra": "0x02E000000000012E",
    "Orisa": "0x02E000000000013E",
    "Doomfist": "0x02E000000000012F",
    "Moira": "0x02E00000000001A2",
    "ALL HEROES": "0x02E00000FFFFFFFF"
}

id_hero = {v: k for k, v in hero_id.items()}

stat_id = {
    "Time Played": "overwatch.guid.0x0860000000000021",
    "Games Won": "overwatch.guid.0x0860000000000039",
    "Win Percentage": "overwatch.guid.0x08600000000003D1",
    "Weapon Accuracy": "overwatch.guid.0x086000000000002F",
    "Eliminations per Life": "overwatch.guid.0x08600000000003D2",
    "Multikill - Best": "overwatch.guid.0x0860000000000346",
    "Objective Kills - Average": "overwatch.guid.0x086000000000039C"
}

id_stat = {v: k for k, v in stat_id.items()}

def parse_career_profile(html: str) -> dict:

    if html == None:
        return None
    
    root = parse(html)
    
    " Parse info from quickplay and competitive."
    def parse_game_mode(mode: etree._Element):
        general_stats = {}
        for stat in mode.xpath('./section/div/div[@data-category-id and @data-group-id="comparisons"]'):
            stat_dict = {}
            for hero in stat:
                bar_description = hero.xpath('./div/div/div[@class="description"]')[0].text
                bar_percentage = hero.get('data-overwatch-progress-percent')
                stat_dict[id_hero[hero.get('data-hero-guid')]] = (bar_description, bar_percentage)
            general_stats[id_stat[stat.get('data-category-id')]] = stat_dict

        hero_stats = {}
        for hero in mode.xpath('./section/div/div[@data-category-id and @data-group-id="stats"]'):
            hero_dict = {}
            for stat_group in hero:
                stat_group_name = stat_group.xpath('./div/table/thead/tr/th/h5[@class="stat-title"]')[0].text
                stat_dict = {}
                for stat in stat_group.xpath('./div/table/tbody')[0]:
                    stat_name = stat[0].text
                    stat_value = stat[1].text
                    stat_dict[stat_name] = stat_value
                hero_dict[stat_group_name] = stat_dict
            hero_stats[id_hero[hero.get('data-category-id')]] = hero_dict

        return {'general_stats': general_stats, 'hero_stats': hero_stats}

    quickplay = root.xpath('./body/div/div/div[@data-mode="quickplay"]')[0]
    competitive = root.xpath('./body/div/div/div[@data-mode="competitive"]')[0]
    
    quickplay_stats = parse_game_mode(quickplay)
    competitive_stats = parse_game_mode(competitive)

    "Parse general info."
    btag_link = root[0].xpath('./meta[@property="og:url"]')[0].get('content')
    btag = re.match(r'^\S+/(\S+)$', btag_link).group(1)

    _rank = root.xpath("./body/div/section/div/div/div/div/div/div/div[@class='competitive-rank']/div")
    if len(_rank) > 0:
        rank = _rank[0].text
    else:
        rank = None

    general_info = {
        'btag': btag,
        'rank': rank
    }
    
    "Compile results in a dict."

    result = {
        'quickplay_stats': quickplay_stats,
        'competitive_stats': competitive_stats,
        'general_info': general_info
    }
    
    return result


" Parse info from quickplay and competitive."

"""
def parse_game_mode(mode: etree._Element):
    general_stats = {}
    for stat in mode.xpath('./section/div/div[@data-category-id and @data-group-id="comparisons"]'):
        stat_dict = {}
        for hero in stat:
            bar_description = hero.xpath('./div/div/div[@class="description"]')[0].text
            bar_percentage = hero.get('data-overwatch-progress-percent')
            stat_dict[id_hero[hero.get('data-hero-guid')]] = (bar_description, bar_percentage)
        general_stats[id_stat[stat.get('data-category-id')]] = stat_dict

    hero_stats = {}
    for hero in mode.xpath('./section/div/div[@data-category-id and @data-group-id="stats"]'):
        hero_dict = {}
        for stat_group in hero:
            stat_group_name = stat_group.xpath('./div/table/thead/tr/th/h5[@class="stat-title"]')[0].text
            stat_dict = {}
            for stat in stat_group.xpath('./div/table/tbody')[0]:
                stat_name = stat[0].text
                stat_value = stat[1].text
                stat_dict[stat_name] = stat_value
            hero_dict[stat_group_name] = stat_dict
        hero_stats[id_hero[hero.get('data-category-id')]] = hero_dict

    return {'general_stats': general_stats, 'hero_stats': hero_stats}
"""

"""
    
f = open('./sample/StarGazer-11683', 'r')
html = f.read()

root = parse(html)
quickplay = root.xpath('.//div[@data-mode="quickplay"]')[0]
competitive = root.xpath('.//div[@data-mode="competitive"]')[0]

print(time.strftime('%X') + (": Begin parse_career_profile(html)."))
for i in range(0, 10000):
    parse_career_profile(html)
print(time.strftime('%X') + (": End."))

print(time.strftime('%X') + (": Begin parse_game_mode()."))
for i in range(0, 10000):
    parse_game_mode(quickplay)
    parse_game_mode(competitive)   
print(time.strftime('%X') + (": End."))

print(time.strftime('%X') + (": Begin xpath."))
for i in range(0, 10000):
    quickplay.xpath('./section/div/div[@data-category-id and @data-group-id="comparisons"]')
print(time.strftime('%X') + (": End."))

print(time.strftime('%X') + (": Begin parse(html)."))
for i in range(0, 10000):
    parse(html)
print(time.strftime('%X') + (": End."))

print(time.strftime('%X') + (": Begin finding rank."))
for i in range(0, 10000):
    root.xpath("./body/div/section/div/div/div/div/div/div/div[@class='competitive-rank']/div")
print(time.strftime('%X') + (": End."))

print(time.strftime('%X') + (": Begin btag."))
for i in range(0, 10000):
    btag_link = root[0].xpath('./meta[@property="og:url"]')[0].get('content')
    btag = re.match(r'^\S+/(\S+)$', btag_link).group(1)
print(time.strftime('%X') + (": End."))

"""
