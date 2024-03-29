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
    ax.plot(x, df8['proposal_rule_weight'], label='prop leb8', c='g')
    ax.plot(x, df16['current_rule_weight'], label='curr eb16', c='r', ls='--')
    ax.plot(x, df16['proposal_rule_weight'], label='prop eb16', c='g', ls='--')
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
    ax.plot(x, df8['knosh_rule_weight'], label='knosh leb8', c='b')
    ax.plot(x, df8['proposal_rule_weight'], label='prop leb8', c='g')
    ax.plot(x, df16['knosh_rule_weight'], label='knosh eb16', c='b', ls='--')
    ax.plot(x, df16['proposal_rule_weight'], label='prop eb16', c='g', ls='--')
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
    ax.plot(df['curr_pie'], ls='', marker='o', alpha=.5, c='r', label='curr')
    ax.plot(df['knosh_pie'], ls='', marker='o', alpha=.5, c='b', label='knosh')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ylims = ax.get_ylim()
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
    ax.legend()
    fig.savefig('./imgs/operators_kc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['knosh_pie'] / df['curr_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ylimsdiff = ax.get_ylim()
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
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
    ax.plot(df['curr_pie'], ls='', marker='o', alpha=.5, c='r', label='curr')
    ax.plot(df['prop_pie'], ls='', marker='o', alpha=.5, c='g', label='prop')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
    ax.legend()
    fig.savefig('./imgs/operators_pc.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['prop_pie'] / df['curr_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_ylim(ylimsdiff)
    ax.set_ylabel('Proposed rule rewards as a percentage\nof Current rule rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
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
    ax.plot(df['prop_pie'], ls='', marker='o', alpha=.5, c='g', label='prop')
    ax.plot(df['knosh_pie'], ls='', marker='o', alpha=.5, c='b', label='knosh')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(ylims)
    ax.set_ylabel('Portion of all Rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
    ax.legend()
    fig.savefig('./imgs/operators_kp.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    ax.plot(df['knosh_pie'] / df['prop_pie'], ls='', marker='o', alpha=.5, c='k')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_ylim(ylimsdiff)
    ax.set_ylabel('Knoshua rule rewards as a percentage\nof Proposed rule rewards')
    ax.set_xlabel('Node (sorted by matched ETH)')
    ax.violinplot(
        (df['knosh_pie'] / df['prop_pie']).dropna(),
        positions=[-200],
        widths=[250],
        showmedians=True,
        showextrema=False)
    ax.grid()
    fig.savefig('./imgs/operatorsdiff_kp.png', bbox_inches='tight')


def apr_and_appreciation():
    ratio_expectation = np.arange(.3, 2.0, .05)

    # hypothetical nodes switching RPL to an LEB8; node is large and at 152% nETH
    #   ppm values come from https://www.desmos.com/calculator/o71k2vz1qt
    before_current152 = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 45544e-6
    after_current152 = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 45620e-6
    swap_yield_current152 = (after_current152 - before_current152) / 8
    before_prop = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 17411e-6
    after_prop = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 17488e-6
    swap_yield_prop = (after_prop - before_prop) / 8
    before_current148 = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 44937e-6
    after_current148 = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 44886e-6
    swap_yield_current148 = (after_current148 - before_current148) / 8

    current_rpl_apr = .7 * .05 * 19.55e6 * .0174 * 45544e-6 / 7300
    worst_proposed_rpl_apr = current_rpl_apr * (0.0308 / 0.0808)

    # get aprs including expectations
    rpl_net_apr_current = 1.0 * (ratio_expectation - 1) + current_rpl_apr * ratio_expectation
    rpl_net_apr_worst_proposed = (
        1.0 * (ratio_expectation - 1) + worst_proposed_rpl_apr * ratio_expectation)

    fig, ax = plt.subplots(1)
    ax.plot(ratio_expectation, rpl_net_apr_current, label='Current', c='r')
    ax.plot(ratio_expectation, rpl_net_apr_worst_proposed, label='Worst Proposed', c='g')
    ax.axhline(swap_yield_current152, label='Swap yield (curr152)', c='r', alpha=0.5, ls='--')
    ax.axhline(swap_yield_current148, label='Swap yield (curr148)', c='r', alpha=0.5, ls=':')
    ax.axhline(swap_yield_prop, label='Swap yield (proposed)', c='g', alpha=0.5, ls='--')
    ax.set_xlabel('Per-year ratio appreciation expectation')
    ax.set_ylabel('Net "APR" including\nper-year ratio appreciation expectation')
    ax.legend()
    ax.grid()
    fig.savefig('./imgs/apr_and_appreciation.png', bbox_inches='tight')
    ax.set_xlim([.8, 1.2])
    ax.set_ylim([-.06, .21])
    fig.savefig('./imgs/apr_and_appreciation_zoom.png', bbox_inches='tight')


def heavy_spend(df_og):
    df = df_og.copy()
    # get amount of spend going to staked RPL beyond 30% pETH
    heavy_cutoff_peth = 0.3
    df['earning_peth_pct'] = df['peth_pct'] * (1.5 / df['neth_pct'])
    df['earning_peth_pct'] = df[['peth_pct', 'earning_peth_pct']].min(axis=1)
    df['heavy_pct'] = df['earning_peth_pct'] - heavy_cutoff_peth
    df['heavy_pct'] = df['heavy_pct'].clip(lower=0)
    df['curr_heavypie'] = df['curr_pie'] * df['heavy_pct']
    print(
        f"Spending on stake beyond {100*heavy_cutoff_peth}% pETH: {100*sum(df['curr_heavypie']):.1f}%"
    )


def top_off(df_og):
    df = df_og.copy()
    df['top_off_rpl_value_in_eth'] = ((.1 / df['peth_pct']) - 1) * df['staked_rpl_value_in_eth']
    df['top_off_rpl_value_in_eth'].clip(lower=0, inplace=True)
    print(
        f"A total of {df['top_off_rpl_value_in_eth'].sum()} ETH worth of RPL would be needed to top everyone off"
    )


def main():
    apr_and_appreciation()

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

    heavy_spend(df)
    top_off(df)

    single_pool_plots(
        curr_total=sum(df['current_rule_weight']),
        knosh_total=sum(df['knosh_rule_weight']),
        prop_total=sum(df['proposal_rule_weight']))

    current_node_plots(df)


if __name__ == '__main__':
    main()
