##From the Console Cowboys Youtube Series
## Uses the Etherscan API to pull down attackers transaction totals accross attackers addresses
##@ficti0n on twitter

import requests, os
from colorama import Fore

api_key = os.getenv('APIKEY')
total_value_recieved = 0
attackers_list = [line.rstrip() for line in open('attackersOutput.txt')]


for count, target_address in enumerate (attackers_list): 
    value_in_address = 0

    #Get Internal Transaction By Address
    etherscan_params = (('module', 'account'), 
                        ('action', 'txlistinternal'),
                        ('address', target_address), 
                        ('sort', 'asc'),
                        ('apikey', api_key))


    response = requests.get("https://api.etherscan.io/api", params=etherscan_params)
    data = response.json().get("result")

    #print(f'{Fore.RED}requesting URL: {response.url}\n')

    for ID, transaction in enumerate(data):
        current_value = int(transaction.get("value"))/1000000000000000000
        total_value_recieved += current_value
        value_in_address += current_value
    print(f'{Fore.WHITE}Value in: {Fore.RED}{target_address} is {Fore.GREEN}{value_in_address}')


print(f'{Fore.YELLOW} Total Contract Value Recieved: {Fore.GREEN}{total_value_recieved}')
