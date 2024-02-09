import pandas as pd


def current_optimum(row):
    # migrate to EB8s as much as possible
    provided = row['matched_eth']
    matched = row['matched_eth']
    while provided * 3 > matched:  # not all eb8 yet
        next_matched = matched + 32
        if row['staked_rpl_value_in_eth'] < .1 * next_matched:
            break
        else:
            matched = next_matched
    return matched


def aggressive(row):
    # 1 EB6, then any number of EB1.5s
    provided = row['provided_eth'] - 6
    matched = 32 - 6
    matched += (provided // 1.5) * (32 - 1.5)
    return matched


def aggressive_alt(row):
    # 2 EB4, then any number of EB1.5s
    provided = row['provided_eth'] - 8
    matched = 2 * (32 - 4)
    matched += (provided // 1.5) * (32 - 1.5)
    return matched


def bit_safer(row):
    # Up to 6 LEB4, then any number of LEB2s
    num_leb4 = min(row['provided_eth'] // 4, 6)
    provided = row['provided_eth'] - num_leb4 * 4
    matched = num_leb4 * (32 - 4)
    matched += (provided // 2) * (32 - 2)
    return matched


def main():
    df = pd.read_csv('staking_snapshot_2.csv')
    df = df[df['provided_eth'] > 0]
    df['matched_eth_current_optimum'] = df.apply(lambda row: current_optimum(row), axis=1)
    df['matched_eth_aggressive'] = df.apply(lambda row: aggressive(row), axis=1)
    df['matched_eth_aggressive_alt'] = df.apply(lambda row: aggressive_alt(row), axis=1)
    df['matched_eth_bit_safer'] = df.apply(lambda row: bit_safer(row), axis=1)
    print(df.sum(axis=0))

    # 2024/02/09 results
    # 591k      matched_eth
    # 942k      matched_eth_current_optimum
    # 3.639M    matched_eth_bit_safer
    # 5.179M    matched_eth_aggressive_alt
    # 5.194M    matched_eth_aggressive


if __name__ == '__main__':
    main()
