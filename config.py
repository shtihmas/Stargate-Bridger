import random

''' Variables you need to change '''
AMOUNT_MIN = 10  # Min amount to bridge
AMOUNT_MAX = 15  # Max amount to bridge
TIMES = 10  # 1 time => Polygon -> Fantom -> Polygon => 2 transactions

''' Variables that should better not be changed '''
AMOUNT_RANDOM = random.randint(AMOUNT_MIN, AMOUNT_MAX)  # Bridge Quantity Randomization
AMOUNT_TO_SWAP = AMOUNT_RANDOM * (10 ** 6)  # Do not change!
SLIPPAGE = 5  # 5 = 0.5%, 10 = 1%, 1 = 0.1%
MIN_AMOUNT = AMOUNT_TO_SWAP - (AMOUNT_TO_SWAP * SLIPPAGE) // 1000  # Do not change!

''' Wallets loading'''
with open('private_keys.txt', 'r') as f:
    WALLETS = [row.strip() for row in f]
