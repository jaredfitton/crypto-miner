# Sources:

# How to calculate coins mined per day
# (1) https://bitcoin.stackexchange.com/questions/13964/explain-the-math-behind-mining-profitability-calculators
# (2) https://arxiv.org/pdf/1112.4980v1.pdf

import requests
import json
import os
from bs4 import BeautifulSoup

def get_coin_earnings(coin):
    '''
    Scrape the coin URL (currently only works for whattomine) and retreive the earnings for that coin.

    TO-DO: Allow different URLs to be used (2crypto, whattomine, etc.)
    '''
    payload = {
        "hr": coin["website"]["config"]["hr"],
        "p": 0,
        "fee": 0,
        "cost": 0,
        "hcost": 0
    }
    page = requests.get(coin["website"]["url"], params=payload)

    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.find_all("td")
    
    # Earnings per hour
    earnings = {
        "est_rewards": data[2].text.strip(),
        "rev_btc": data[3].text.strip(),
        "rev_usd": data[4].text.strip(),
    }

    return earnings



def calculate_coins_earned(symbol):
    config = json.loads(open("config.json").read())
    r = requests.get(f'https://whattomine.com/coins/{symbol}.json')

    # Convert the json from the request into a dictionary
    mining_stats = json.loads(r.text)

    br = mining_stats["block_reward"]
    d = mining_stats["difficulty24"]
    
    hr = config["hashrate_hs"]
    t = config["time_s"]

    # Calculate the amount of coins earned in the specific amount of time, t
    return (hr * t * br * 100000) // (d) / 100000

def convert(symbol, amount):
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD,BTC&api_key={os.getenv("WHAT_TO_MINE_API_KEY")}')
    coin_conversions = json.loads(r.text)
    usd = coin_conversions["USD"] * amount
    btc = coin_conversions["BTC"] * amount
    return (usd, btc)