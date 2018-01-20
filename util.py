import re

from algorithm.trie import Trie

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

def scramble_name(name: str):
    return [
        name,
        name.upper(),
        name.capitalize()
        ]
"""
with open('./data/btags.txt', 'r') as btag_file:
    btags = btag_file.read().split("\n")
    while btags[-1] == '':
        btags = btags[:-1]

with open('/usr/share/dict/words', 'r') as word_file:
    words = word_file.read().split("\n")
    while words[-1] == '':
        words = words[:-1]
        
extract_name = re.compile('(\S+)-\d+')
names = []
for btag in btags:
    names.append(extract_name.match(btag).group(1))

count = 0
for name in names:
    if name[0].isupper() and name[1:].islower() and name.isalpha():
        count = count + 1

two_words = re.compile('([A-Z][a-z]+)([A-Z][a-z]+)')
count = 0
for name in names:
    if two_words.match(name) is not None:
        count += 1

trie = Trie()
for word in words:
    word = word.lower()
    if word in 'bcdefghjklmnopqrstuvwxyz':
        continue
    if word.isalpha():
        trie.insert(word)

        
prefix = []
for name in names:
    name = name.lower()
    matches = trie.match_prefix(name)
    if len(matches) > 1:
        prefix.append(matches[-1])

tokens = []
count = 0
for name in names:
    name = name.lower()
    matches = trie.match_all(name)
    if len(matches) > 0 and len(matches) < 3:
        tokens.append(matches)


def min_split(l):
    min_s = None
    min_l = 10000
    for i in l:
        if len(i) < min_l:
            min_s = i
            min_l = len(i)
    return min_s

optimal = list(map(min_split, tokens))
parts = []
for l in optimal:
    parts.extend(l)

"""
