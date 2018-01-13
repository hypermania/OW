import aiohttp
import asyncio
import requests
import time
import json
from concurrent.futures import ProcessPoolExecutor


from parsing import parse_career_profile
from conversion import convert_parsed
from util import convert_time

PROFILE_URL = 'https://playoverwatch.com/en-us/career/pc/{}'
    
async def fetch(client):
    async with client.get(PROFILE_URL.format(btags[0])) as resp:
        assert resp.status == 200
        return await resp.text()


async def fetch_btag(client, btag):
    async with client.get(PROFILE_URL.format(btag)) as resp:
        if resp.status == 200:
            return await resp.text()

        if resp.status == 404:
            return None

        raise Exception('unknown error')


async def process_html(client, btag, lock, sem, count):

    await sem.acquire()

    while True:
        try:
            html = await fetch_btag(client, btag)
            break
        except:
            continue
    
    parsed = await loop.run_in_executor(p, parse_career_profile, html)
    try:
        convert_parsed(parsed)
    except:
        print("An error occured in conversion for btag {}.".format(btag))
    
    if parsed == None:
        sem.release()
        return None

    await lock.acquire()
    save_file.write('{}\n'.format(json.dumps(parsed)))
    count[0] = count[0] + 1
    if count[0] % 100 == 0:
        print(time.strftime('%X') + (": Obtained %d profiles." % count[0]))
    lock.release()

    sem.release()
    
            
async def main():

    async with aiohttp.ClientSession(read_timeout=10, conn_timeout=10) as client:

        lock = asyncio.Lock()
        sem = asyncio.Semaphore(200)
        
        tasks = []
        for btag in btags:
            task = asyncio.ensure_future(process_html(client, btag, lock, sem, count))
            tasks.append(task)
        await asyncio.gather(*tasks)


with open('./data/btags.txt', 'r') as btag_file:
    btags = btag_file.read().split("\n")
    while btags[-1] == '':
        btags = btags[:-1]
        

count = [0]
save_file = open('./data/dumps.json', 'w')
p = ProcessPoolExecutor(4)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


