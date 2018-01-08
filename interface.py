import aiohttp
import asyncio
import requests

from parsing import parse_career_profile


with open('./data/btags.txt', 'r') as btag_file:
    btags = btag_file.read().split("\n")[:-1]

PROFILE_URL = 'https://playoverwatch.com/en-us/career/pc/{}'
    
async def fetch(client):
    async with client.get(PROFILE_URL.format(btags[0])) as resp:
        assert resp.status == 200
        return await resp.text()

async def fetch_btag(client, btag):
    async with client.get(PROFILE_URL.format(btag)) as resp:
        if resp.status == 200:
            return await resp.text()
        else:
            print("Error for btag:{} resp.status = {}".format(btag, resp.status))

async def process_html(client, btag, lock, ranks):
    html = await fetch_btag(client, btag)
    
    parsed = parse_career_profile(html)
    
    if parsed == None:
        return None
    
    rank_str = parsed["general_info"]["rank"]
    if rank_str == None:
        return None

    return int(rank_str)
    
ranks = []        
            
async def main():
    """
    async with aiohttp.ClientSession() as client:

        tasks = []
        for btag in btags[0:1000]:
            task = asyncio.ensure_future(process_html(client, btag, lock, ranks))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

        print(ranks)
    """
        
            
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


ranks = []
for btag in btags[0:10000]:
    r = requests.get(PROFILE_URL.format(btag))
    if r.status_code == 200:
        parsed = parse_career_profile(r.text)
    
        if parsed == None:
            continue
    
        rank_str = parsed["general_info"]["rank"]
        if rank_str == None:
            continue

        ranks.append(int(rank_str))

        if len(ranks) % 10 == 0:
            print(len(ranks))
        
