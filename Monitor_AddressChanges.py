##From the Console Cowboys Youtube Series
## Monitors for address changes on smart contract we were auditing
##@ficti0n on twitter

import requests, re, time
from datetime import datetime

attackers_list = [line.rstrip() for line in open('attackersOutput.txt')]

def checkAddresses():
    response = requests.get("https://raw.githubusercontent.com/uniswaprouter3/mempool/main/v3")
    data = response.text
    attackerAddress = re.search(r'return (.*?);', data).group(1)
    now = datetime.now()
    timeUpdated = now.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    if attackerAddress not in attackers_list:
        attackers_list.append(attackerAddress)
        writeAddress(attackerAddress, timeUpdated)

def writeAddress(attackerAddress, timeUpdated):
    with open("attackersOutput.txt", 'a') as writer:
        writer.write(attackerAddress + "\n")

    with open('attackerAddress.csv', 'a') as writer:
        writer.write(attackerAddress+","+timeUpdated + "\n")
    print(f' New address {attackerAddress} logged at {timeUpdated} \n')

def main():
    while(True):
        checkAddresses()
        time.sleep(300)
        


if __name__ == "__main__":
    main()
