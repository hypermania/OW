import json
import re

def load_btag_file(filename):
    _generated_btags = open(filename, 'r')
    generated_btags = _generated_btags.read().split('\n')
    while generated_btags[-1] == '':
        generated_btags = generated_btags[:-1]
    return generated_btags

    
_wordlist = load_btag_file('./data/wordlist_generated_btags.txt')
_generator = load_btag_file('./data/generated_btags_reduced.txt')
_first_name = load_btag_file('./data/first_name_generated_btags.txt')
_scraped = load_btag_file('./data/btags.txt')

all_btags = _wordlist + _generator + _first_name + _scraped
all_btags = sorted(list(set(all_btags)))

btags_output = open('./data/btags_sum.txt', 'a')
for btag in all_btags:
    btags_output.write("{}\n".format(btag))
btags_output.close()
