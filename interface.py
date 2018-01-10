import aiohttp
import asyncio
import requests
import time
from concurrent.futures import ProcessPoolExecutor


from parsing import parse_career_profile
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


async def process_html(client, btag, lock, ranks, sem):

    await sem.acquire()

    while True:
        try:
            html = await fetch_btag(client, btag)
            break
        except:
            continue
    
    #parsed = yield from loop.run_in_executor(parse_career_profile(html))
    parsed = await loop.run_in_executor(p, parse_career_profile, html)
    
    if parsed == None:
        sem.release()
        return None
    
    #rank_str = parsed["general_info"]["rank"]
    time_str = parsed["quickplay_stats"]["general_stats"]["Time Played"]["Mercy"][0]
    total_time = convert_time(time_str)
    
    if total_time == None:
        sem.release()
        return None

    await lock.acquire()
    ranks.append(total_time)
    
    if len(ranks) % 100 == 0:
        print(time.strftime('%X') + (": Obtained %d ranks." % len(ranks)))
        
    lock.release()

    sem.release()

    return total_time
    
            
async def main():

    async with aiohttp.ClientSession(read_timeout=10, conn_timeout=10) as client:

        lock = asyncio.Lock()
        sem = asyncio.Semaphore(100)
        
        tasks = []
        for btag in btags:
            task = asyncio.ensure_future(process_html(client, btag, lock, ranks, sem))
            tasks.append(task)
        await asyncio.gather(*tasks)

        print(ranks)

with open('./data/btags.txt', 'r') as btag_file:
    btags = btag_file.read().split("\n")
    while btags[-1] == '':
        btags = btags[:-1]
        
ranks = []

p = ProcessPoolExecutor(4)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


