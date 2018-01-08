from io import FileIO
import json
import re

btags = FileIO('btags.json')
btags = json.load(btags)

btags2 = FileIO('btags2.json')
btags2 = json.load(btags2)

btags3 = FileIO('btags3.json')
btags3 = json.load(btags3)

btags4 = FileIO('btags4.json')
btags4 = json.load(btags4)

btags.extend(btags2)
btags.extend(btags3)
btags.extend(btags4)

extract = re.compile(r'\S+/pc/../(\S+)')

result = set()

for d in btags:
    link = d['link']
    match = extract.match(link)
    if match is not None:
        result.add(match.group(1))


result = sorted(list(result))

f = open("btags.txt", mode='w')
for btag in result:
    f.write("{}\n".format(btag))

    
