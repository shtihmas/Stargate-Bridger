import json
import random
import asyncio
from web3 import AsyncWeb3
from web3.providers.async_rpc import AsyncHTTPProvider
from config import WALLETS, AMOUNT_TO_SWAP, TIMES, MIN_AMOUNT


polygon_rpc_url = 'https://polygon-rpc.com/'
fantom_rpc_url = 'https://rpc.ftm.tools/'

polygon_w3 = AsyncWeb3(AsyncHTTPProvider(polygon_rpc_url))
fantom_w3 = AsyncWeb3(AsyncHTTPProvider(fantom_rpc_url))

stargate_polygon_address = polygon_w3.to_checksum_address('0x45A01E4e04F14f7A4a6702c74187c5F6222033cd')
stargate_fantom_address = fantom_w3.to_checksum_address('0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6')

stargate_abi = json.load(open('router_abi.json'))
usdc_abi = json.load(open('usdc_abi.json'))

usdc_polygon_address = polygon_w3.to_checksum_address('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174')
usdc_fantom_address = fantom_w3.to_checksum_address('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')

stargate_polygon_contract = polygon_w3.eth.contract(address=stargate_polygon_address, abi=stargate_abi)
stargate_fantom_contract = fantom_w3.eth.contract(address=stargate_fantom_address, abi=stargate_abi)

usdc_polygon_contract = polygon_w3.eth.contract(address=usdc_polygon_address, abi=usdc_abi)
usdc_fantom_contract = fantom_w3.eth.contract(address=usdc_fantom_address, abi=usdc_abi)


async def swap_usdc_polygon_to_fantom(wallet):

    account = polygon_w3.eth.account.from_key(wallet)
    address = account.address
    nonce = await polygon_w3.eth.get_transaction_count(address)
    gas_price = await polygon_w3.eth.gas_price
    fees = await stargate_fantom_contract.functions.quoteLayerZeroFee(112,
                                                                1,
                                                                "0x0000000000000000000000000000000000001010",
                                                                "0x",
                                                                [0, 0, "0x0000000000000000000000000000000000000001"]
                                                                ).call()
    fee = fees[0]

    allowance = await usdc_polygon_contract.functions.allowance(address, stargate_polygon_address).call()

    if allowance < AMOUNT_TO_SWAP:

        approve_txn = await usdc_polygon_contract.functions.approve(stargate_polygon_address, AMOUNT_TO_SWAP).build_transaction({
            'from': address,
            'gas': 150000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })
        signed_approve_txn = polygon_w3.eth.account.sign_transaction(approve_txn, wallet)
        approve_txn_hash = await polygon_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

        print(f"POLYGON | USDT APPROVED https://polygonscan.com/tx/{approve_txn_hash.hex()}")
        nonce += 1

        await asyncio.sleep(30)

    usdc_balance = await usdc_polygon_contract.functions.balanceOf(address).call()

    if usdc_balance >= AMOUNT_TO_SWAP:

        chainId = 112
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = account.address
        amountIn = AMOUNT_TO_SWAP
        amountOutMin = MIN_AMOUNT
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = account.address
        data = '0x'

        swap_txn = await stargate_polygon_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).build_transaction({
            'from': address,
            'value': fee,
            'gas': 500000,
            'gasPrice': await polygon_w3.eth.gas_price,
            'nonce': await polygon_w3.eth.get_transaction_count(address),
        })

        signed_swap_txn = polygon_w3.eth.account.sign_transaction(swap_txn, wallet)
        swap_txn_hash = await polygon_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        return swap_txn_hash

    elif usdc_balance < AMOUNT_TO_SWAP:

        min_amount = usdc_balance - (usdc_balance * 5) // 1000

        chainId = 112
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = account.address
        amountIn = usdc_balance
        amountOutMin = min_amount
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = account.address
        data = '0x'

        swap_txn = await stargate_polygon_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).build_transaction({
            'from': address,
            'value': fee,
            'gas': 500000,
            'gasPrice': await polygon_w3.eth.gas_price,
            'nonce': await polygon_w3.eth.get_transaction_count(address),
        })

        signed_swap_txn = polygon_w3.eth.account.sign_transaction(swap_txn, wallet)
        swap_txn_hash = await polygon_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        return swap_txn_hash


async def swap_usdc_fantom_to_polygon(wallet):

    account = fantom_w3.eth.account.from_key(wallet)
    address = account.address
    nonce = await fantom_w3.eth.get_transaction_count(address)
    gas_price = await fantom_w3.eth.gas_price
    fees = await stargate_fantom_contract.functions.quoteLayerZeroFee(109,
                                                       1,
                                                       "0x0000000000000000000000000000000000000001",
                                                       "0x",
                                                       [0, 0, "0x0000000000000000000000000000000000000001"]
                                                       ).call()
    fee = fees[0]

    allowance = await usdc_fantom_contract.functions.allowance(address, stargate_fantom_address).call()

    if allowance < AMOUNT_TO_SWAP:

        approve_txn = await usdc_fantom_contract.functions.approve(stargate_fantom_address, AMOUNT_TO_SWAP).build_transaction({
            'from': address,
            'gas': 150000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })
        signed_approve_txn = fantom_w3.eth.account.sign_transaction(approve_txn, wallet)
        approve_txn_hash = await fantom_w3.eth.send_raw_transaction(signed_approve_txn.rawTransaction)

        print(f"FANTOM | USDC APPROVED | https://ftmscan.com/tx/{approve_txn_hash.hex()} ")
        nonce += 1

        await asyncio.sleep(30)

    usdc_balance = await usdc_fantom_contract.functions.balanceOf(address).call()

    if usdc_balance >= AMOUNT_TO_SWAP:

        chainId = 109
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = account.address
        amountIn = AMOUNT_TO_SWAP
        amountOutMin = MIN_AMOUNT
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = account.address
        data = '0x'

        swap_txn = await stargate_fantom_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).build_transaction({
            'from': address,
            'value': fee,
            'gas': 600000,
            'gasPrice': await fantom_w3.eth.gas_price,
            'nonce': await fantom_w3.eth.get_transaction_count(address),
        })

        signed_swap_txn = fantom_w3.eth.account.sign_transaction(swap_txn, wallet)
        swap_txn_hash = await fantom_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        return swap_txn_hash

    elif usdc_balance < AMOUNT_TO_SWAP:

        min_amount = usdc_balance - (usdc_balance * 5) // 1000

        chainId = 109
        source_pool_id = 1
        dest_pool_id = 1
        refund_address = account.address
        amountIn = usdc_balance
        amountOutMin = min_amount
        lzTxObj = [0, 0, '0x0000000000000000000000000000000000000001']
        to = account.address
        data = '0x'

        swap_txn = await stargate_fantom_contract.functions.swap(
            chainId, source_pool_id, dest_pool_id, refund_address, amountIn, amountOutMin, lzTxObj, to, data
        ).build_transaction({
            'from': address,
            'value': fee,
            'gas': 600000,
            'gasPrice': await fantom_w3.eth.gas_price,
            'nonce': await fantom_w3.eth.get_transaction_count(address),
        })

        signed_swap_txn = fantom_w3.eth.account.sign_transaction(swap_txn, wallet)
        swap_txn_hash = await fantom_w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        return swap_txn_hash


async def check_balance(address, usdc_contract):

    usdc_balance = await usdc_contract.functions.balanceOf(address).call()
    return usdc_balance


async def balance_update(address, usdc_contract):
    balance = await check_balance(address, usdc_contract)

    while balance < 3 * (10 ** 6):
        await asyncio.sleep(10)
        balance = await check_balance(address, usdc_contract)

    return True


async def work(wallet):
    counter = 0

    account = polygon_w3.eth.account.from_key(wallet)
    address = account.address

    start_delay = random.randint(1, 200)
    await asyncio.sleep(start_delay)

    while counter < TIMES:

        balance = None
        while not balance:
            await asyncio.sleep(10)
            balance = await balance_update(address, usdc_polygon_contract)

        polygon_to_fantom_txn_hash = await swap_usdc_polygon_to_fantom(wallet)
        print(f"POLYGON | {address} | Transaction: https://polygonscan.com/tx/{polygon_to_fantom_txn_hash.hex()}")

        polygon_delay = random.randint(1200, 1500)
        await asyncio.sleep(polygon_delay)

        balance = None
        while not balance:
            await asyncio.sleep(10)
            balance = await balance_update(address, usdc_fantom_contract)

        fantom_to_polygon_txn_hash = await swap_usdc_fantom_to_polygon(wallet)
        print(f"FTM | {address} | Transaction: https://ftmscan.com/tx/{fantom_to_polygon_txn_hash.hex()}")

        fantom_delay = random.randint(100, 300)
        await asyncio.sleep(fantom_delay)

        counter += 1

    print(f'Wallet: {address} | DONE')


async def main():
    tasks = []
    for wallet in WALLETS:
        tasks.append(asyncio.create_task(work(wallet)))

    for task in tasks:
        await task

    print(f'*** ALL JOB IS DONE ***')


if __name__ == '__main__':
    asyncio.run(main())
