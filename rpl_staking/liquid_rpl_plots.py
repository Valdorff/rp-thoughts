import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from reward_plots import current_rules, proposal_rules


def main():
    df = pd.read_csv('staking_snapshot_2.csv')
    df = df[df['provided_eth'] > 0]
    df['neth_pct'] = df['staked_rpl_value_in_eth'] / df['provided_eth']
    df['peth_pct'] = df['staked_rpl_value_in_eth'] / df['matched_eth']
    df['current_rule_weight'] = df.apply(lambda row: current_rules(row), axis=1)
    df['proposal_rule_weight'] = df.apply(lambda row: proposal_rules(row), axis=1)
    df['curr_pie'] = df['current_rule_weight'] / sum(df['current_rule_weight'])
    df['prop_pie'] = df['proposal_rule_weight'] / sum(df['proposal_rule_weight'])
    df.sort_values(['matched_eth'], inplace=True)
    df.reset_index(inplace=True)

    assert np.isclose(sum(df['curr_pie']), 1)
    assert np.isclose(sum(df['prop_pie']), 1)

    # index will now be withdrawal address
    df = df.groupby('withdrawal_address').agg(
        staked_rpl_value_in_eth=('staked_rpl_value_in_eth', np.sum),
        provided_eth=('provided_eth', np.sum),
        matched_eth=('matched_eth', np.sum),
        current_rule_weight=('current_rule_weight', np.sum),
        proposal_rule_weight=('proposal_rule_weight', np.sum),
        curr_pie=('curr_pie', np.sum),
        prop_pie=('prop_pie', np.sum),
        liquid_rpl_node_value_in_eth=('liquid_rpl_node_value_in_eth', np.sum),
        # avoid double-counting RPL in withdrawal address
        liquid_rpl_withdrawal_value_in_eth=('liquid_rpl_withdrawal_value_in_eth', np.mean),
        # not exact if nodes in a withdrawal address are differently sized; bad estimate, which we redo below
        peth_pct=('peth_pct', np.mean),
        neth_pct=('neth_pct', np.mean),
    )

    # add patricio liquid RPL manually
    df.at['0x92a510f62A2A2b608b37179f909186F9A048bc92',
          'liquid_rpl_node_value_in_eth'] = 949711.98 * .017

    # redoing these percents now that we've grouped...
    df['neth_pct'] = df['staked_rpl_value_in_eth'] / df['provided_eth']
    df['neth_pct_no_yield'] = (df['neth_pct'] - 1.5).clip(
        lower=0)  # part 1; then we need liquid rpl
    df['peth_pct'] = df['staked_rpl_value_in_eth'] / df['matched_eth']

    df['liquid_rpl_value_in_eth'] = (
        df['liquid_rpl_node_value_in_eth'] + df['liquid_rpl_withdrawal_value_in_eth'])
    df['liquid_staked_proportion'] = df['liquid_rpl_value_in_eth'] / df['staked_rpl_value_in_eth']
    df['neth_pct_no_yield'] += df['liquid_rpl_value_in_eth'] / df[
        'provided_eth']  # part 2; includes both over-150% and liquid

    # liquid RPL plot
    fig, ax = plt.subplots(1)
    clipped = df['liquid_staked_proportion'].clip(upper=4)
    ax.scatter(df['neth_pct'], clipped, alpha=0.1)
    # noinspection PyTupleAssignmentBalance
    m, b = np.polyfit(df['neth_pct'], df['liquid_staked_proportion'], 1)
    # noinspection PyTupleAssignmentBalance
    m2, b2 = np.polyfit(df[df['neth_pct'] < 1.5]['neth_pct'],
                        df[df['neth_pct'] < 1.5]['liquid_staked_proportion'], 1)
    ax.plot(df['neth_pct'], m * df['neth_pct'] + b, color='k', alpha=0.6, label='fit line')
    ax.plot(
        df['neth_pct'],
        m2 * df['neth_pct'] + b2,
        color='gray',
        alpha=0.6,
        label='fit line considering only up to 150% nETH holders')
    ax.set_xlabel('Staked RPL, as % bonded ETH')
    ax.set_ylabel(
        'liquid_rpl / effective_staked_rpl\n(liquid on node/withdrawal addresses or over 150%)')
    ax.legend()
    fig.savefig('./imgs/liquid_rpl.png', bbox_inches='tight')

    # pie chart of the different groups of withdrawal addresses
    df['category'] = 'potential_sensitives'
    # note that these categorizations need to be in reverse priority order
    df.loc[df['prop_pie'] > df['curr_pie'], 'category'] = 'rewards_increase'
    df.loc[df['neth_pct_no_yield'] > 0.05, 'category'] = 'insensitive_bulls'
    df.loc[df['peth_pct'] < .1, 'category'] = 'below_threshold'
    df['potsens_sensitive_rpl_value_in_eth'] = 0.
    df['potsens_insensitive_rpl_value_in_eth'] = 0.

    # find the point at which rewards APR is now better than current; that portion is insensitive
    total_proposal_weight = df['proposal_rule_weight'].sum()
    tempdf = df.copy()
    for i in range(len(tempdf)):
        row = tempdf.iloc[i].copy()
        if row['category'] != 'potential_sensitives':
            continue
        accepted_pie_per_rpl = row['curr_pie'] / row['staked_rpl_value_in_eth']
        row['staked_rpl_value_in_eth'] = row['staked_rpl_value_in_eth'] + row[
            'liquid_rpl_value_in_eth']
        while ((proposal_rules(row) / total_proposal_weight) /
               row['staked_rpl_value_in_eth']) < accepted_pie_per_rpl:
            if row['staked_rpl_value_in_eth'] - 8 < max(0.15 * row['matched_eth'], 0.10 * (row['matched_eth'] + 24)):
                break
            row['staked_rpl_value_in_eth'] -= 8
            row['matched_eth'] += 24
            row['peth_pct'] = row['staked_rpl_value_in_eth'] / row['matched_eth']

        df.at[df.index[i], 'potsens_insensitive_rpl_value_in_eth'] = row['staked_rpl_value_in_eth']
        df.at[df.index[i], 'potsens_sensitive_rpl_value_in_eth'] = (
            df.iloc[i]['staked_rpl_value_in_eth'] + df.iloc[i]['liquid_rpl_value_in_eth'] -
            row['staked_rpl_value_in_eth'])

    labels = ['below_threshold', 'insensitive_bulls', 'rewards_increase', 'potential_sensitives']
    labels2 = labels + ['potsens:insensitive_part', 'unstaked_other']

    ct_sizes = []
    rplct_sizes = []
    for lbl in labels:
        tempdf = df[df['category'] == lbl]
        ct_sizes.append(1.0 * len(tempdf))
        if lbl == 'potential_sensitives':
            rplct_sizes.append(tempdf['potsens_sensitive_rpl_value_in_eth'].sum())
        else:
            rplct_sizes.append(tempdf['staked_rpl_value_in_eth'].sum() +
                               tempdf['liquid_rpl_value_in_eth'].sum())
    rplct_sizes.append(df[df['category'] == 'potential_sensitives']
                       ['potsens_insensitive_rpl_value_in_eth'].sum())  # insensitive RPL
    rplct_sizes.append(19547495.7 * 0.017 - sum(rplct_sizes))  # RPL outside the system
    fig, subs = plt.subplots(1, 2)
    subs[0].pie(ct_sizes, autopct='%1.1f%%')
    subs[1].pie(rplct_sizes, autopct='%1.1f%%')
    subs[1].legend(labels2, bbox_to_anchor=(0.75, .1), ncol=2)
    subs[0].set_title('By NO count')
    subs[1].set_title('By RPL weight')
    fig.savefig('./imgs/category_pies.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
