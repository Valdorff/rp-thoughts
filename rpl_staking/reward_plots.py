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


# The one I'm currently favoring
def proposal_rules(row):
    if row['staked_rpl_value_in_eth'] < (0.1 * row['matched_eth']):
        return 0
    if row['staked_rpl_value_in_eth'] < (0.15 * row['matched_eth']):
        return (100 * row['peth_pct']) * row['matched_eth']
    return (15 - 1.3863 + 2 * np.log(100 * row['peth_pct'] - 13)) * row['matched_eth']


def single_pool_plots(curr_total, knosh_total, prop_total):
    x = np.arange(0, 32, .1)
    df8 = pd.DataFrame({
        'staked_rpl_value_in_eth': x,
        'provided_eth': [8] * len(x),
        'matched_eth': [24] * len(x)
    })
    df8['neth_pct'] = df8['staked_rpl_value_in_eth'] / df8['provided_eth']
    df8['peth_pct'] = df8['staked_rpl_value_in_eth'] / df8['matched_eth']
    df8['current_rule_weight'] = df8.apply(lambda row: current_rules(row), axis=1)
    df8['current_rule_weight'] /= curr_total
    df8['knosh_rule_weight'] = df8.apply(lambda row: knosh_rules(row), axis=1)
    df8['knosh_rule_weight'] /= knosh_total
    df8['proposal_rule_weight'] = df8.apply(lambda row: proposal_rules(row), axis=1)
    df8['proposal_rule_weight'] /= prop_total

    df16 = pd.DataFrame({
        'staked_rpl_value_in_eth': x,
        'provided_eth': [16] * len(x),
        'matched_eth': [16] * len(x)
    })
    df16['neth_pct'] = df16['staked_rpl_value_in_eth'] / df16['provided_eth']
    df16['peth_pct'] = df16['staked_rpl_value_in_eth'] / df16['matched_eth']
    df16['current_rule_weight'] = df16.apply(lambda row: current_rules(row), axis=1)
    df16['current_rule_weight'] /= curr_total
    df16['knosh_rule_weight'] = df16.apply(lambda row: knosh_rules(row), axis=1)
    df16['knosh_rule_weight'] /= knosh_total
    df16['proposal_rule_weight'] = df16.apply(lambda row: proposal_rules(row), axis=1)
    df16['proposal_rule_weight'] /= prop_total

    # all rules
    fig, subs = plt.subplots(3, sharex='all', sharey='all')
    subs[0].plot(x, df8['current_rule_weight'], label='leb8', c='r')
    subs[1].plot(x, df8['knosh_rule_weight'], label='leb8', c='b')
    subs[2].plot(x, df8['proposal_rule_weight'], label='leb8', c='g')
    subs[0].plot(x, df16['current_rule_weight'], label='eb16', c='r', ls='--')
    subs[1].plot(x, df16['knosh_rule_weight'], label='eb16', c='b', ls='--')
    subs[2].plot(x, df16['proposal_rule_weight'], label='eb16', c='g', ls='--')
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
    fig.savefig('./imgs/rule_summary.png', bbox_inches='tight')

    # knoshua vs current
    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['current_rule_weight'], label='curr leb8', c='r')
    ax.plot(x, df8['knosh_rule_weight'], label='knosh leb8', c='b')
    ax.plot(x, df16['current_rule_weight'], label='curr eb16', c='r', ls='--')
    ax.plot(x, df16['knosh_rule_weight'], label='knosh eb16', c='b', ls='--')
    fmt = mtick.FuncFormatter(ppm)
    ax.set_yticks([0, .00005, .0001, .00015])
    ax.yaxis.set_major_formatter(fmt)
    ax.grid()
    ax.legend()
    ax.set_ylabel('ppm of rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rule_kc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['knosh_rule_weight'] / df8['current_rule_weight'], label='leb8', c='k')
    ax.plot(
        x, df16['knosh_rule_weight'] / df16['current_rule_weight'], label='eb16', c='k', ls='--')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.grid()
    ax.legend()
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rulediff_kc.png', bbox_inches='tight')

    # prop vs current
    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['current_rule_weight'], label='curr leb8', c='r')
    ax.plot(x, df8['proposal_rule_weight'], label='prop leb8', c='b')
    ax.plot(x, df16['current_rule_weight'], label='curr eb16', c='r', ls='--')
    ax.plot(x, df16['proposal_rule_weight'], label='prop eb16', c='b', ls='--')
    fmt = mtick.FuncFormatter(ppm)
    ax.set_yticks([0, .00005, .0001, .00015])
    ax.yaxis.set_major_formatter(fmt)
    ax.grid()
    ax.legend()
    ax.set_ylabel('ppm of rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rule_pc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['proposal_rule_weight'] / df8['current_rule_weight'], label='leb8', c='k')
    ax.plot(
        x, df16['proposal_rule_weight'] / df16['current_rule_weight'], label='eb16', c='k', ls='--')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.grid()
    ax.legend()
    ax.set_ylabel('Proposed rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rulediff_pc.png', bbox_inches='tight')

    # knosh vs prop
    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['knosh_rule_weight'], label='knosh leb8', c='r')
    ax.plot(x, df8['proposal_rule_weight'], label='prop leb8', c='b')
    ax.plot(x, df16['knosh_rule_weight'], label='knosh eb16', c='r', ls='--')
    ax.plot(x, df16['proposal_rule_weight'], label='prop eb16', c='b', ls='--')
    fmt = mtick.FuncFormatter(ppm)
    ax.set_yticks([0, .00005, .0001, .00015])
    ax.yaxis.set_major_formatter(fmt)
    ax.grid()
    ax.legend()
    ax.set_ylabel('ppm of rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rule_kp.png', bbox_inches='tight')

    fig, ax = plt.subplots(1, sharex='all', sharey='all')
    ax.plot(x, df8['knosh_rule_weight'] / df8['proposal_rule_weight'], label='leb8', c='k')
    ax.plot(
        x, df16['knosh_rule_weight'] / df16['proposal_rule_weight'], label='eb16', c='k', ls='--')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.grid()
    ax.legend()
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Proposed rule rewards')
    ax.set_xlabel('Staked RPL Value in ETH')
    fig.savefig('./imgs/rulediff_kp.png', bbox_inches='tight')


def current_node_plots(df):
    # knoshua vs current
    fmt = mtick.FuncFormatter(ppmpct)
    fig, ax = plt.subplots(1)
    ax.plot(df['curr_pie'], ls='', marker='o', alpha=.5, c='r')
    ax.plot(df['knosh_pie'], ls='', marker='o', alpha=.5, c='b')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ylims = ax.get_ylim()
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('./imgs/operators_kc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['knosh_pie'] / df['curr_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ylimsdiff = ax.get_ylim()
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Matched ETH')
    ax.violinplot(
        (df['knosh_pie'] / df['curr_pie']).dropna(),
        positions=[-200],
        widths=[250],
        showmedians=True,
        showextrema=False)
    ax.grid()
    fig.savefig('./imgs/operatorsdiff_kc.png', bbox_inches='tight')

    # prop vs current
    fig, ax = plt.subplots(1)
    ax.plot(df['curr_pie'], ls='', marker='o', alpha=.5, c='r')
    ax.plot(df['prop_pie'], ls='', marker='o', alpha=.5, c='g')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('./imgs/operators_pc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['prop_pie'] / df['curr_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_ylim(ylimsdiff)
    ax.set_ylabel('Proposed rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Matched ETH')
    ax.violinplot(
        (df['prop_pie'] / df['curr_pie']).dropna(),
        positions=[-200],
        widths=[250],
        showmedians=True,
        showextrema=False)
    ax.grid()
    fig.savefig('./imgs/operatorsdiff_pc.png', bbox_inches='tight')

    # knosh vs prop
    fig, ax = plt.subplots(1)
    ax.plot(df['prop_pie'], ls='', marker='o', alpha=.5, c='g')
    ax.plot(df['knosh_pie'], ls='', marker='o', alpha=.5, c='b')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Matched ETH')
    fig.savefig('./imgs/operators_kp.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['knosh_pie'] / df['prop_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_ylim(ylimsdiff)
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Proposed rule rewards')
    ax.set_xlabel('Matched ETH')
    ax.violinplot(
        (df['knosh_pie'] / df['prop_pie']).dropna(),
        positions=[-200],
        widths=[250],
        showmedians=True,
        showextrema=False)
    ax.grid()
    fig.savefig('./imgs/operatorsdiff_kp.png', bbox_inches='tight')


def main():
    df = pd.read_csv('staking_snapshot.csv')
    df = df[df['provided_eth'] > 0]
    df['neth_pct'] = df['staked_rpl_value_in_eth'] / df['provided_eth']
    df['peth_pct'] = df['staked_rpl_value_in_eth'] / df['matched_eth']
    df['current_rule_weight'] = df.apply(lambda row: current_rules(row), axis=1)
    df['knosh_rule_weight'] = df.apply(lambda row: knosh_rules(row), axis=1)
    df['proposal_rule_weight'] = df.apply(lambda row: proposal_rules(row), axis=1)
    df['curr_pie'] = df['current_rule_weight'] / sum(df['current_rule_weight'])
    df['knosh_pie'] = df['knosh_rule_weight'] / sum(df['knosh_rule_weight'])
    df['prop_pie'] = df['proposal_rule_weight'] / sum(df['proposal_rule_weight'])
    df.sort_values(['matched_eth'], inplace=True)
    df.reset_index(inplace=True)

    assert np.isclose(sum(df['curr_pie']), 1)
    assert np.isclose(sum(df['knosh_pie']), 1)
    assert np.isclose(sum(df['prop_pie']), 1)

    single_pool_plots(
        curr_total=sum(df['current_rule_weight']),
        knosh_total=sum(df['knosh_rule_weight']),
        prop_total=sum(df['proposal_rule_weight']))

    current_node_plots(df)
    plt.show()


if __name__ == '__main__':
    main()
