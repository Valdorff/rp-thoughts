import os
import time

import pandas as pd
from web3 import HTTPProvider, Web3

API_KEY = os.environ['INFURA']
CLIENT = Web3(HTTPProvider(f"https://mainnet.infura.io/v3/{API_KEY}"))

RocketNetworkPricesV4 = CLIENT.eth.contract(
    address=Web3.to_checksum_address("0x25E54Bf48369b8FB25bB79d3a3Ff7F3BA448E382"),
    abi=
    '[{"inputs":[{"internalType":"contract RocketStorageInterface","name":"_rocketStorageAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"slotTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesSubmitted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"slotTimestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesUpdated","type":"event"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_slotTimestamp","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"}],"name":"executeUpdatePrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPricesBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRPLPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_slotTimestamp","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"}],"name":"submitPrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'
)

RocketNetworkPricesV2 = CLIENT.eth.contract(
    address=Web3.to_checksum_address("0x751826b107672360b764327631cC5764515fFC37"),
    abi=
    '[{"inputs":[{"internalType":"contract RocketStorageInterface","name":"_rocketStorageAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesSubmitted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesUpdated","type":"event"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"}],"name":"executeUpdatePrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getLatestReportableBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPricesBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRPLPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"}],"name":"submitPrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'
)

RocketNetworkPricesV1 = CLIENT.eth.contract(
    address=Web3.to_checksum_address("0xd3f500F550F46e504A4D2153127B47e007e11166"),
    abi=
    '[{"inputs":[{"internalType":"contract RocketStorageInterface","name":"_rocketStorageAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"effectiveRplStake","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesSubmitted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rplPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"effectiveRplStake","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"PricesUpdated","type":"event"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"decreaseEffectiveRPLStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"},{"internalType":"uint256","name":"_effectiveRplStake","type":"uint256"}],"name":"executeUpdatePrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getEffectiveRPLStake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEffectiveRPLStakeUpdatedBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLatestReportableBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPricesBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRPLPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"inConsensus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"increaseEffectiveRPLStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_block","type":"uint256"},{"internalType":"uint256","name":"_rplPrice","type":"uint256"},{"internalType":"uint256","name":"_effectiveRplStake","type":"uint256"}],"name":"submitPrices","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'
)

evt_ls = []

ls = RocketNetworkPricesV1.events.PricesUpdated().get_logs(
    argument_filters={},
    fromBlock=13325250,
    toBlock=17066950,
)
evt_ls += [(evt.args.time, evt.args.rplPrice) for evt in ls]

time.sleep(1)
ls = RocketNetworkPricesV2.events.PricesUpdated().get_logs(
    argument_filters={},
    fromBlock=17066920,
    toBlock=20102500,
)
evt_ls += [(evt.args.time, evt.args.rplPrice) for evt in ls]

time.sleep(1)
ls = RocketNetworkPricesV4.events.PricesUpdated().get_logs(
    argument_filters={},
    fromBlock=20102480,
    toBlock='latest',
)
evt_ls += [(evt.args.time, evt.args.rplPrice) for evt in ls]

epocht_ls, rplprice_ls = zip(*evt_ls)
dt_ls = pd.to_datetime(epocht_ls, unit='s')
df = pd.DataFrame(data={'datetime': dt_ls, 'rpl_price': rplprice_ls})
df.to_csv('rpl_price_history.csv')
