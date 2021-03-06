import requests
import json

config = json.loads(open("config.json").read())

earnings = []

# Constant Parameters
hr = config["hashrate_hs"]
t = config["time_s"]

for coin in config["coins"]:
    r = requests.get(f'https://whattomine.com/coins/{coin["id"]}.json')

    mining_stats = json.loads(r.text)

    br = mining_stats["block_reward"]
    d = mining_stats["difficulty24"]

    coins_per_t = (hr * t * br * 100000) // (2**32 * d) / 100000

    # print("")
    # print("Block Reward: " + str(br))
    # print("Difficulty: " + str(d))
    # print("Time: " + str(t) + " seconds")
    # print("Hash Rate: " + str(hr) + " h/s")

    # print("----------------------------------")
    # print(f"Coins per {t} seconds: {coins_per_t}")

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={coin["symbol"]}&tsyms=USD,BTC&api_key=a52bbc5bc6968dc2430d817f993c403ede2815915cfdd4e38859631a2233e22f')

    eth_conversion = json.loads(r.text)
    revenue_usd = eth_conversion["USD"] * coins_per_t
    revenue_btc = eth_conversion["BTC"] * coins_per_t

    earnings.append([coin["name"], coin["symbol"], coins_per_t, revenue_btc, revenue_usd])

    # print("Revenue (USD): " + str(revenue_usd))
    # print("Revenue (BTC): " + str(revenue_btc))



# Print all of the coin earnings in a table format
print("\n")
print(f"Time (seconds): {t}")
print(f"Hashrate (h/s): {hr}")
print("\n")
print("{:<12} {:<10} {:<15} {:<10} {:<15}".format('Name','Symbol','Coins Earned','Rev. BTC', 'Rev. USD'))
for coin in earnings:
    print("{:<12} {:<10} {:<15} {:<10} {:<15}".format(coin[0], coin[1], round(coin[2], 9), round(coin[3], 6), round(coin[4], 3)))

# Final print to separate last output from command line prompt
print("\n")