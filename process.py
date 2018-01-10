from io import FileIO
import json
import re

_generated_btags = open('./data/generated_btags.txt', 'r')
generated_btags = _generated_btags.read().split('\n')
while generated_btags[-1] == '':
    generated_btags = generated_btags[:-1]
generated_btags = list(set(generated_btags))

save_file = open('./data/generated_btags_processed.txt', 'w')
for btag in generated_btags:
    save_file.write("{}\n".format(btag))
