## First Draft Version of MakeMeASandwhich.py by CC labs / Console Cowboys
## @ficti0n on twitter
# From the Console Cowboys Blockchain Forensics Youtube Series (link below)
#https://www.youtube.com/watch?v=LI4PrsqzORE&list=PLCwnLq3tOElrUdIg4LgdhPhCKAiy7NZYA
## Uses the web3.py API to pull down transactions in the latest block
## Then finds likily bot activity and then parses out Frontrunning and Sandwich attacks


from web3 import Web3
from colorama import Fore

#------------------------Setup Variables and Connections--------------------#
web3 = Web3(Web3.HTTPProvider(''))
block = web3.eth.get_block('latest')
toFromPairs = {}
transactionCount = {}
txLookup = {}
possibleSandwich = {}
#------------------------ End Setup Variables and Connections---------------#

def grabTransactions():
    """ Pull down all transactions and create dictionaries of counts 
    related to  To/From Address Pairs and associated hashes
    Dictionaries Created: 
          transactioncount To:count, 
          toFromPairs To:From, 
          txLookup Txhash[to,from,gas]"""
    #Grab our Transactions and thier transaction hashes
    if block and block.transactions: 
        for transaction in block.transactions: 
            tempTXDict = {}
            tx_hash = transaction.hex() # Convert txhashes from hexBytes format
            tx = web3.eth.get_transaction(tx_hash)

    #Check if To/From pairs exist and update count        
            if tx.to != None:
                if tx.to in toFromPairs:
                    if toFromPairs[tx.to] == tx["from"]:
                        transactionCount[tx.to] = transactionCount[tx.to] +1 
                        txLookup[tx_hash] =  [tx.to,tx["from"],tx.gasPrice]

    #Start a running count on any new To addresses and create a to/from pair               
                elif tx.to not in toFromPairs:
                    transactionCount[tx.to] = 1
                    toFromPairs[tx.to] = tx["from"]
                    txLookup[tx_hash] =  [tx.to,tx["from"],tx.gasPrice]

              
def findBots():
    """Grab all to/from pairs with exactly 2 transactions in a single block 
       for review and create possibleSandwich dictionary txhash:[to,gas]"""
    for transactionHash, pair in txLookup.items():    
        if transactionCount[pair[0]] == 2:
            possibleSandwich[transactionHash] = [pair[0],pair[2]]   

            
def findSandwich(possibleSandwich): 
    """This function takes in a dictionary with a value list hash:[to,gas] 
    of possible sandwhich attacks with 2 transactions and Parses for gas 
    variance to remove bots which keep sending via the same gas calulation"""
    #Dicitionaries to swap and parse out duplicates and return valid attacks
    allBots = {}
    duplicateBots = {}
    sandwiches = []

    #Checks for duplicate gas values as these cannot be sandwich attacks and can be removed
    #These are parsed into total lists of bots and duplicates
    for sHash, sGas in possibleSandwich.items(): 
        if sGas[1] in allBots.values():
            #print(f"Adding {sGas[1]} to duplicate bots")
            duplicateBots[sHash] = sGas[1]
        
        elif sGas[1] not in allBots.values():    
            #print(f"Adding {sGas[1]} to all bots")
            allBots[sHash] = sGas[1]
    print(f'{len(allBots)} bot transactions parsed with 2 like pairs')
    print('---------------------------------------------------------')
    for bot in allBots.keys():
        print(bot)
    print('---------------------------------------------------------')


    #Grabs all transactions gas prices which are bots but not in duplicateBots 
    for sHash, bot in allBots.items():
        if duplicateBots:
            if bot not in duplicateBots.values():
               sandwiches.append(sHash) 

    return sandwiches           
 

if __name__ == "__main__":
#Setup Transactions and bot dictionaries for parsing
    grabTransactions()
    findBots()

#Throws possible sandwhich pairs through the sandwich algo
#Then returns and prints anything that matches
    if possibleSandwich:
        sandwiches =findSandwich(possibleSandwich)
        for sandwich in sandwiches:
            print(f'{Fore.GREEN}Delicious Sandwich Found: \n {Fore.YELLOW}{sandwich}')        
            
