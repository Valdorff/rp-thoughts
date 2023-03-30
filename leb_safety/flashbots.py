from collections import defaultdict
import gzip
import json
import logging
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# raw data from https://flashbots-boost-relay-public.s3.us-east-2.amazonaws.com/index.html
RAW_DIR: Optional[Path] = None  # use only processed data
# RAW_DIR = Path(r'D:\Rocket Pool\Flashbots data')  # process raw data into processed, as neeed
PROCESSED_DIR = Path(__file__).parent / 'Flashbots best reward'


def parse_data():
    net = {}
    for path in sorted(RAW_DIR.glob('*.json.gz')):
        log.info(path.name)
        processed_path = PROCESSED_DIR / path.name

        try:
            with gzip.open(processed_path) as fp:
                d = json.load(fp)
            d = {int(k): v for k, v in d.items()}
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with gzip.open(path) as fp:
                ls = json.load(fp)

            d = {}
            for lsd in ls:
                block = int(lsd['block_number'])
                if (block not in d.keys()) or (int(lsd['value']) > d[block]):
                    d[block] = float(int(lsd['value']) / 1e18)

            with gzip.open(processed_path, 'w') as fp:
                fp.write(json.dumps(d).encode('utf-8'))

        net.update(d)
    return net


def parse_processed_data():
    net = {}
    for path in sorted(PROCESSED_DIR.glob('*.json.gz')):
        log.info(path.name)

        with gzip.open(path) as fp:
            d = json.load(fp)
        d = {int(k): v for k, v in d.items()}
        net.update(d)
    return net


def main(percentiles=(50, 99, 99.5, 99.9, 99.99), penalties=tuple()):
    if RAW_DIR is None:
        net = parse_processed_data()
    else:
        net = parse_data()
    log.info(f'{len(net)} data files')
    blocks, values = zip(*list(net.items()))
    week = []
    results = defaultdict(list)
    survival_results = defaultdict(list)  # value over this percentile
    beyond_penalty_results = defaultdict(list)  # assuming penalty

    ct = 0
    # for start in range(min(blocks), max(blocks) + 1, 50400 // 4):  # 50400 blocks is a week
    for start in range(min(blocks), max(blocks) + 1, 50400):  # 50400 blocks is a week
        ct += 1
        week.append(ct)
        ls = np.array([value for block, value in net.items() if start <= block < start + 50400])
        total = sum(ls)
        for i, percentile in enumerate(percentiles):
            tmp = np.percentile(ls, percentile)
            results[percentile].append(tmp)
            survival_results[percentile].append(sum(ls[ls > tmp]) / total)
            if len(penalties) == len(percentiles):
                # subtract out penalty from each block and sum any that still had losses
                tmp = ls[ls > tmp] - penalties[i]
                beyond_penalty_results[percentile].append(sum(tmp[tmp > 0]) / total)

    for percentile in percentiles:
        log.info(
            f'{percentile}%ile N({np.mean(results[percentile])}, {np.std(results[percentile])})')
        plt.plot(week, results[percentile], label=f'{percentile}%ile')
    plt.ylabel('Percent of blocks above a specific percentile')
    plt.xlabel('Week (starting at the merge)')
    plt.legend()
    plt.grid()

    plt.subplots(1)
    for percentile in percentiles:
        plt.plot(week, 100 * np.array(survival_results[percentile]), label=f'{percentile}%ile')
        print(percentile, np.mean(survival_results[percentile]))
    plt.ylabel('Percent of total value above a specific percentile')
    plt.xlabel('Week (starting at the merge)')
    plt.legend()
    plt.grid()

    if len(penalties) == len(percentiles):
        plt.subplots(1)
        for percentile in percentiles:
            plt.plot(
                week, 100 * np.array(beyond_penalty_results[percentile]), label=f'{percentile}%ile')
            print(percentile, np.mean(beyond_penalty_results[percentile]))
        plt.ylabel('Percent of total value above a specific percentile\nbeyond what penalty covers')
        plt.xlabel('Week (starting at the merge)')
        plt.legend()
        plt.grid()

    plt.show()


if __name__ == '__main__':
    log = logging.getLogger('log')
    log.setLevel(logging.DEBUG)  # Leave this on DEBUG
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter('%(levelname)-10s %(asctime)s %(message)-140s'))
    log.addHandler(sh)
    sh.setLevel(logging.DEBUG)  # Change as desired
    log.info('starting')

    # main(percentiles=(50, ))
    main(percentiles=(99.7, 99.83, 99.9), penalties=(6.8, 8, 10.4))
