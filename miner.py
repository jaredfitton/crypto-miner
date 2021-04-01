import requests
import json
import sys
import os

from dotenv import load_dotenv
from formulas import *
from helpers import *

def get_lowest_order(algo, market):
    r = requests.get(f"https://api2.nicehash.com/main/api/v2/public/orders?algorithm={algo}&market={market}")

    orders_json = json.loads(r.text)
    orders = orders_json["list"]

    if len(orders) == 0:
        sys.exit("There are no orders.")

    # Search the current active orders to find the order with the lowest price with active miners (rigsCount)
    lowest_order = {
        "price": sys.maxsize
    }
    for order in orders:
        if order["alive"] and order["rigsCount"] > 0 and float(order["price"]) < float(lowest_order["price"]):
            lowest_order = order

    return lowest_order

def execute_order(coin):
    print("Creating order...")

if __name__ == "__main__":
    config = json.loads(open("config.json").read())

    earnings = []

    for coin in config["coins"]:
        # Calculate the amount of coins earned in the specific amount of time, t
        coin_earnings = get_coin_earnings(coin)

        amount = coin["nicehash"]["order_cost"] - coin["nicehash"]["fee"]
        limit = coin["nicehash"]["limit"]
        lowest_order = get_lowest_order(coin["nicehash"]["algo"], coin["nicehash"]["market"])
        price = float(lowest_order["price"])

        mining_duration = amount * 24 / (price * limit)
        revenue = mining_duration * float(coin_earnings["rev_btc"])
        profit = (revenue - coin["nicehash"]["order_cost"])*(1-coin["misc_fee_percent"])
        roi = profit / coin["nicehash"]["order_cost"] * 100

        earnings.append([coin["name"], coin["symbol"], mining_duration, revenue, profit, roi])

    print_earnings_table(earnings)

    while(True):
        selection = input("Enter 'quit' or the id of the coin you would like to create an order for: ")
        print("")

        if selection == "quit":
            os._exit(0)

        try:
            id = int(selection)
        except:
            print(f"{selection} is not a number, try again\n")
            continue

        if id < 0 or id > len(earnings)-1:
            print(f"{selection} is not a valid ID, try again\n")
            continue
        
        confirmation = input(f"Are you sure you want to create an order for {earnings[id][0]}? (y/n): ")
        print("")

        if confirmation == "y":
            execute_order(earnings[id])
            break
        elif confirmation == "n":
            continue
        else:
            print("Invalid input, try again\n")

print("\n")


