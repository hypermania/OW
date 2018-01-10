import aiohttp
import asyncio
import time
import re
import uvloop

from lxml import etree

from util import check_name


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

PROFILE_URL = 'https://playoverwatch.com/en-us/career/pc/{}'
    
async def check_existence(client, btag, sem):
    await sem.acquire()

    while True:
        try:
            async with client.get(PROFILE_URL.format(btag)) as resp:
                if resp.status == 404:
                    result = None
                else:
                    result = btag
            break
        except:
            continue

    sem.release()
    return result

async def main():
    sem = asyncio.Semaphore(500)
    
    async with aiohttp.ClientSession(read_timeout=10, conn_timeout=10) as client:
        count = 0
        for name in names:
            tasks = []
            for num in nums:
                btag = "{}-{}".format(name, num)
                task = asyncio.ensure_future(check_existence(client, btag, sem))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            result = list(filter(lambda x: x is not None, result))
            for btag in result:
                btag_save_file.write("{}\n".format(btag))
            btag_save_file.flush()
            
            count = count + 1            
            print(time.strftime('%X') + ": Finished name {}. ({}/{})".format(name, count, 1295))

            
nums = list(range(1000, 5000))
nums.extend(list(range(11000,12000)))
nums.extend(list(range(21000,22000)))
nums.extend(list(range(31000,32000)))
nums.extend(list(range(41000,42000)))

"""
_first = open('./dict/first.txt', 'r')
_second = open('./dict/second.txt', 'r')

first = _first.read().split('\n')
second = _second.read().split('\n')

while first[-1] == '':
    first = first[:-1]
while second[-1] == '':
    second = second[:-1]

names = []
for a in first:
    for b in second:
        names.append(a + b)
"""

_names = open('./dict/google-10000-english.txt', 'r')
names = _names.read().split('\n')
while names[-1] == '':
    names = names[:-1]
names = list(filter(check_name, names))

btag_save_file = open('./data/list_generated_btags.txt', 'a')

#last_btag = btag_file.read().split("\n")[:-1][-1]
#last_name = re.match('(\S+)-\d+', last_btag)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
