import aiohttp
import asyncio
import time
import re

from lxml import etree

from util import check_name

import uvloop

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

    conn = aiohttp.TCPConnector(limit=0, force_close=True)
    
    async with aiohttp.ClientSession(read_timeout=10, conn_timeout=10, connector=conn) as client:
        count = 0
        count_found = 0
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

            count += 1
            count_found += len(result)
            print(time.strftime('%X') + ": Finished name {}. (finished {} name, found {})".format(name, count, count_found))


            
nums = list(range(1000, 5000))
nums.extend(list(range(11000,12000)))
nums.extend(list(range(21000,22000)))
nums.extend(list(range(31000,32000)))
nums.extend(list(range(41000,42000)))


_names = open('./dict/random-name-master/first-names.txt', 'r')
names = _names.read().split('\n')
while names[-1] == '':
    names = names[:-1]
names = list(filter(check_name, names))
print("Loaded {} names.".format(len(names)))

"""
extended_names = []
for name in names:
    extended_names.append(name)
    extended_names.append(name.upper())
    extended_names.append(name.capitalize())
names = extended_names
"""


btag_save_file = open('./data/first_name_generated_btags.txt', 'a')

print(time.strftime('%X') + ": Begin loop.")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
