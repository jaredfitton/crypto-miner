import os

def print_earnings_table(data):
    header = "{:<5} {:<25} {:<18} {:<22} {:<22} {:<22} {:<22}".format('Id', 'Name', 'Symbol', "Duration (Hours)", "Rev. BTC", "Profit BTC", "ROI")
    print("-"*(len(header) + 4))
    print(f"| {header} |")
    print("-"*(len(header) + 4))
    for i, coin in enumerate(data):
        print("| {:<5} {:<25} {:<18} {:<22} {:<22} {:<22} {:<22} |".format(i, coin[0], coin[1], round(coin[2], 3), round(coin[3], 8), round(coin[4], 7), str(round(coin[5], 3))+"%"))
    print("-"*(len(header) + 4))

# print_config_details(config)
# print_earnings_table(data)

# while(True):
#     selection = input("Enter 'quit' or the id of the coin you would like to create an order for: ")
#     print("")

#     if selection == "quit":
#         os._exit(0)

#     try:
#         id = int(selection)
#     except:
#         print(f"{selection} is not a number, try again\n")
#         continue

#     if id < 0 or id > len(data)-1:
#         print(f"{selection} is not a valid ID, try again\n")
#         continue
    
#     confirmation = input(f"Are you sure you want to create an order for {data[id][0]}? (y/n): ")
#     print("")

#     if confirmation == "y":
#         break
#     elif confirmation == "n":
#         continue
#     else:
#         print("Invalid input, try again\n")