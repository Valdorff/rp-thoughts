import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def ppm(x, _pos):
    return f'{int(x*1e6)}'


def ppmpct(x, _pos):
    if x > 0.001:
        return f'{int(x * 1e2)}%'
    else:
        return f'{int(x*1e6)} ppm'


def current_rules(row):
    if row['staked_rpl_value_in_eth'] < (0.1 * row['matched_eth']):
        return 0
    elif row['staked_rpl_value_in_eth'] > (1.5 * row['provided_eth']):
        return 1.5 * row['provided_eth']
    else:
        return row['staked_rpl_value_in_eth']


def knosh_rules(row):
    if row['staked_rpl_value_in_eth'] < (0.1 * row['matched_eth']):
        return 0
    else:
        return 0.1 * row['matched_eth']


def proposal_rules(row):
    if row['staked_rpl_value_in_eth'] < (0.1 * row['matched_eth']):
        return 0
    if row['staked_rpl_value_in_eth'] < (0.15 * row['matched_eth']):
        return (100 * row['peth_pct']) * row['matched_eth']
    return (15 - 1.3863 + 2 * np.log(100 * row['peth_pct'] - 13)) * row['matched_eth']


def single_pool_plots(curr_total, knosh_total, prop_total):
    # ruleset plots
    fig, subs = plt.subplots(3, sharex='all', sharey='all')
    x = np.arange(0, 32, .1)
    dftemp = pd.DataFrame({
        'staked_rpl_value_in_eth': x,
        'provided_eth': [8] * len(x),
        'matched_eth': [24] * len(x)
    })
    dftemp['neth_pct'] = dftemp['staked_rpl_value_in_eth'] / dftemp['provided_eth']
    dftemp['peth_pct'] = dftemp['staked_rpl_value_in_eth'] / dftemp['matched_eth']
    dftemp['current_rule_weight'] = dftemp.apply(lambda row: current_rules(row), axis=1)
    dftemp['knosh_rule_weight'] = dftemp.apply(lambda row: knosh_rules(row), axis=1)
    dftemp['proposal_rule_weight'] = dftemp.apply(lambda row: proposal_rules(row), axis=1)
    subs[0].plot(x, dftemp['current_rule_weight'] / curr_total, label='leb8')
    subs[1].plot(x, dftemp['knosh_rule_weight'] / knosh_total, label='leb8')
    subs[2].plot(x, dftemp['proposal_rule_weight'] / prop_total, label='leb8')
    dftemp = pd.DataFrame({
        'staked_rpl_value_in_eth': x,
        'provided_eth': [16] * len(x),
        'matched_eth': [16] * len(x)
    })
    dftemp['neth_pct'] = dftemp['staked_rpl_value_in_eth'] / dftemp['provided_eth']
    dftemp['peth_pct'] = dftemp['staked_rpl_value_in_eth'] / dftemp['matched_eth']
    dftemp['current_rule_weight'] = dftemp.apply(lambda row: current_rules(row), axis=1)
    dftemp['knosh_rule_weight'] = dftemp.apply(lambda row: knosh_rules(row), axis=1)
    dftemp['proposal_rule_weight'] = dftemp.apply(lambda row: proposal_rules(row), axis=1)
    subs[0].plot(x, dftemp['current_rule_weight'] / curr_total, label='eb16')
    subs[1].plot(x, dftemp['knosh_rule_weight'] / knosh_total, label='eb16')
    subs[2].plot(x, dftemp['proposal_rule_weight'] / prop_total, label='eb16')
    fmt = mtick.FuncFormatter(ppm)
    for sub in subs:
        sub.set_yticks([0, .00005, .0001, .00015])
        sub.yaxis.set_major_formatter(fmt)
        sub.grid()
        sub.legend()
    subs[0].set_ylabel('Current Rules\nppm of rewards')
    subs[1].set_ylabel('Knoshua Rules\nppm of rewards')
    subs[2].set_ylabel('Proposed Rules\nppm of rewards')
    subs[2].set_xlabel('Staked RPL Value in ETH')
    fig.savefig('single_pool_plots.png', bbox_inches='tight')


def main():
    df = pd.read_csv('staking_snapshot.csv')
    df = df[df['provided_eth'] > 0]
    df['neth_pct'] = df['staked_rpl_value_in_eth'] / df['provided_eth']
    df['peth_pct'] = df['staked_rpl_value_in_eth'] / df['matched_eth']
    df['current_rule_weight'] = df.apply(lambda row: current_rules(row), axis=1)
    df['knosh_rule_weight'] = df.apply(lambda row: knosh_rules(row), axis=1)
    df['proposal_rule_weight'] = df.apply(lambda row: proposal_rules(row), axis=1)
    # df.sort_values(['current_rule_weight'], inplace=True)
    df.sort_values(['matched_eth'], inplace=True)

    curr_pie = list(df['current_rule_weight'] / sum(df['current_rule_weight']))
    knosh_pie = list(df['knosh_rule_weight'] / sum(df['knosh_rule_weight']))
    prop_pie = list(df['proposal_rule_weight'] / sum(df['proposal_rule_weight']))

    single_pool_plots(
        curr_total=sum(df['current_rule_weight']),
        knosh_total=sum(df['knosh_rule_weight']),
        prop_total=sum(df['proposal_rule_weight']))

    fmt = mtick.FuncFormatter(ppmpct)
    fig, ax = plt.subplots(1)
    ax.plot(curr_pie, ls='', marker='o', alpha=.5, c='r')
    ax.plot(knosh_pie, ls='', marker='o', alpha=.5, c='b')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ylims = ax.get_ylim()
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('current_vs_knoshua.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(curr_pie, ls='', marker='o', alpha=.5, c='r')
    ax.plot(prop_pie, ls='', marker='o', alpha=.5, c='g')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('current_vs_prop.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(prop_pie, ls='', marker='o', alpha=.5, c='g')
    ax.plot(knosh_pie, ls='', marker='o', alpha=.5, c='b')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('knosh_vs_prop.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
