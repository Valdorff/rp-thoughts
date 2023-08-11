import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

from reward_plots import current_rules, proposal_rules


def intended_spend(curr_pie_d, prop_pie_d):
    # Looking at intervals 12-14
    # Data from https://docs.google.com/spreadsheets/d/1jA51myEsuqxhdJyYaBmFvt4RR5RVluPjk1Wl8OCt8Uw/edit#gid=0
    # but used 34.1% for IMC and 20.5% for GMC to align with intent

    # These charts are quite hand-tuned on colors etc; be advised if messing with them

    pdao = 48557.21
    odao = 17657.17
    no = 154500.22
    net = pdao + odao + no
    dev_odao = 3923.82
    dev_pdao = 3584
    imc = 16555.06
    gmc = 9939.49
    reserves = 22062.66
    assert np.isclose(imc + gmc + reserves, pdao)

    fig, ax = plt.subplots(1)
    ax.bar('Node Operators', no / net, width=0.5)
    temp = ax.bar('oDAO', dev_odao / net, width=0.5, label='Dev')
    dev_color = temp[0].properties()['facecolor']
    ax.bar('oDAO', (odao - dev_odao) / net, width=0.5, bottom=dev_odao / net)
    ax.bar('pDAO', dev_pdao / net, width=0.5, color=dev_color)
    ax.bar('pDAO', imc / net, width=0.5, bottom=dev_pdao / net, label='IMC')
    ax.bar('pDAO', gmc / net, width=0.5, bottom=(dev_pdao + imc) / net, label='GMC')
    ax.bar(
        'pDAO', (reserves - dev_pdao) / net,
        width=0.5,
        bottom=(dev_pdao + imc + gmc) / net,
        label='Reserves (non-dev)')
    ax.legend()
    fig.savefig('./imgs/overall_spend_bar.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    pie_weights = [
        no,
        dev_pdao + dev_odao,
        odao - dev_odao,
        imc,
        gmc,
        reserves - dev_pdao,
    ]
    pie_weights = [int(wt * 1000) for wt in pie_weights]
    pie_labels = ['NOs', 'Dev', 'oDAO (non-dev)', 'IMC', 'GMC', 'Reserves (non-dev)']
    overall_spend_patches, _, _ = ax.pie(
        pie_weights, labels=pie_labels, autopct='%1.1f%%', pctdistance=.85)
    fig.savefig('./imgs/overall_spend_pie.png', bbox_inches='tight')

    c_ls = ['LightSkyBlue', 'DodgerBlue', overall_spend_patches[0].get_fc()]
    colors = [c_ls[0]] + [c_ls[1]] * 3 + [c_ls[2]] * (len(curr_pie_d) - 4)
    leg_handles = [
        mpatches.Patch(color=c_ls[0], label='Incentivizing Minipools'),
        mpatches.Patch(color=c_ls[1], label='1.5-3x Overshoot'),
        mpatches.Patch(color=c_ls[2], label='Speculation'),
    ]

    # bar plots showing NO spend
    fig, ax = plt.subplots(1)
    xx = [0.5 * (int(k.split('-')[0]) + int(k.split('-')[1])) for k in curr_pie_d.keys()]
    bins = [int(k.split('-')[0]) for k in curr_pie_d.keys()] + [150]
    _n, _bins, patches = ax.hist(xx, bins=bins, weights=curr_pie_d.values(), rwidth=1.0)
    for i, patch in enumerate(patches):
        patch.set_fc(colors[i])
        patch.set_ec(colors[i])
    ax.set_xlabel('% of Borrowed ETH')
    ax.set_ylabel('% of NO Rewards')
    ax.legend(handles=leg_handles)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    fig.suptitle('Current Spend per Bin')
    fig.savefig('./imgs/no_bar_bins_curr.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    xx = [0.5 * (int(k.split('-')[0]) + int(k.split('-')[1])) for k in prop_pie_d.keys()]
    bins = [int(k.split('-')[0]) for k in prop_pie_d.keys()] + [150]
    _n, _bins, patches = ax.hist(xx, bins=bins, weights=prop_pie_d.values(), rwidth=1.0)
    for i, patch in enumerate(patches):
        patch.set_fc(colors[i])
        patch.set_ec(colors[i])
    ax.set_xlabel('% of Borrowed ETH')
    ax.set_ylabel('% of NO Rewards')
    ax.legend(handles=leg_handles)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    fig.suptitle('Proposed Spend per Bin')
    fig.savefig('./imgs/no_bar_bins_prop.png', bbox_inches='tight')

    # pie plots showing NO spend
    fig, ax = plt.subplots(1)
    vals = list(curr_pie_d.values())
    pie_labels = [
        '10-15%\n(incentivizing minipools)', '15-30%\n(1.5-3x overshoot)', '>30%\n(speculation)'
    ]
    no_curr_pie_weights = [vals[0], sum(vals[1:4]), sum(vals[4:])]
    ax.pie(no_curr_pie_weights, labels=pie_labels, colors=c_ls, autopct='%1.1f%%', pctdistance=.8)
    fig.suptitle('Current spend per RPL category (in % of borrowed ETH)')
    fig.savefig('./imgs/no_pie_bins_curr.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    vals = list(prop_pie_d.values())
    pie_labels = [
        '10-15%\n(incentivizing minipools)', '15-30%\n(1.5-3x overshoot)', '>30%\n(speculation)'
    ]
    no_prop_pie_weights = [vals[0], sum(vals[1:4]), sum(vals[4:])]
    ax.pie(no_prop_pie_weights, labels=pie_labels, colors=c_ls, autopct='%1.1f%%', pctdistance=.8)
    fig.suptitle('Proposed spend per RPL category (in % of borrowed ETH)')
    fig.savefig('./imgs/no_pie_bins_prop.png', bbox_inches='tight')

    # pie plots showing all spend including NO spend categorized
    fig, ax = plt.subplots(1)
    pie_weights = [
        no * (no_curr_pie_weights[0] / sum(no_curr_pie_weights)),
        no * (no_curr_pie_weights[1] / sum(no_curr_pie_weights)),
        no * (no_curr_pie_weights[2] / sum(no_curr_pie_weights)),
        dev_pdao + dev_odao,
        odao - dev_odao,
        imc,
        gmc,
        reserves - dev_pdao,
    ]
    pie_weights = [int(wt * 1000) for wt in pie_weights]
    pie_labels = [
        'NOs (incentivizing minipools)', 'NOs (1.5-3x overshoot)', 'NOs (speculation)', 'Dev',
        'oDAO (non-dev)', 'IMC', 'GMC', 'Reserves (non-dev)'
    ]
    patches, _, _ = ax.pie(pie_weights, labels=pie_labels, autopct='%1.1f%%', pctdistance=.85)
    for i, p in enumerate(patches[:3]):
        p.set_fc(c_ls[i])
    for i, p in enumerate(patches[3:]):
        p.set_fc(overall_spend_patches[i + 1].get_fc())
    fig.suptitle('Current Spend')
    fig.savefig('./imgs/overall_spend_pie_curr.png', bbox_inches='tight')

    fig, ax = plt.subplots(1)
    pie_weights = [
        no * (no_prop_pie_weights[0] / sum(no_prop_pie_weights)),
        no * (no_prop_pie_weights[1] / sum(no_prop_pie_weights)),
        no * (no_prop_pie_weights[2] / sum(no_prop_pie_weights)),
        dev_pdao + dev_odao,
        odao - dev_odao,
        imc,
        gmc,
        reserves - dev_pdao,
    ]
    pie_weights = [int(wt * 1000) for wt in pie_weights]
    pie_labels = [
        'NOs (incentivizing minipools)', 'NOs (1.5-3x overshoot)', 'NOs (speculation)', 'Dev',
        'oDAO (non-dev)', 'IMC', 'GMC', 'Reserves (non-dev)'
    ]
    patches, _, _ = ax.pie(pie_weights, labels=pie_labels, autopct='%1.1f%%', pctdistance=.85)
    for i, p in enumerate(patches[:3]):
        p.set_fc(c_ls[i])
    for i, p in enumerate(patches[3:]):
        p.set_fc(overall_spend_patches[i + 1].get_fc())
    fig.suptitle('Proposed Spend')
    fig.savefig('./imgs/overall_spend_pie_prop.png', bbox_inches='tight')

    plt.show()


def no_spending_by_bin():
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

    # spend per bin of borrowed ETH in portion of the total pie
    # Note: I'm abusing that dictionary key order _is_ preserved, despite not being guaranteed
    #       could use an OrderedDict if one really wants, but then I lose the nice comprehension
    curr_pie_d = {f'{lowend}-{lowend+5}': 0 for lowend in range(10, 146, 5)}
    prop_pie_d = {f'{lowend}-{lowend+5}': 0 for lowend in range(10, 146, 5)}

    for index, row in df.iterrows():
        if row['peth_pct'] < 0.1:
            continue

        curr_pie_so_far = 0
        prop_pie_so_far = 0
        for lowend in range(10, 146, 5):
            k = f'{lowend}-{lowend+5}'
            if (row['peth_pct'] < ((lowend + 5) / 100)) or (lowend == 145):
                # meant to be hit every time -- note that this means 145-150 is really 145+
                curr_pie_d[k] += row['curr_pie'] - curr_pie_so_far
                prop_pie_d[k] += row['prop_pie'] - prop_pie_so_far
                break
            temprow = {
                'matched_eth': row['matched_eth'],
                'provided_eth': row['provided_eth'],
                'peth_pct': ((lowend + 5) / 100),
                'staked_rpl_value_in_eth': ((lowend + 5) / 100) * row['matched_eth'],
            }
            curr_pie_in_bin = ((current_rules(temprow) / row['current_rule_weight']) *
                               row['curr_pie']) - curr_pie_so_far
            curr_pie_d[k] += curr_pie_in_bin
            curr_pie_so_far += curr_pie_in_bin

            prop_pie_in_bin = ((proposal_rules(temprow) / row['proposal_rule_weight']) *
                               row['prop_pie']) - prop_pie_so_far
            prop_pie_d[k] += prop_pie_in_bin
            prop_pie_so_far += prop_pie_in_bin

    # check that I didn't fail to count or double count any
    # print(sum(curr_pie_d.values()))
    # print(sum(prop_pie_d.values()))
    assert np.isclose(sum(curr_pie_d.values()), 1)
    assert np.isclose(sum(prop_pie_d.values()), 1)

    return curr_pie_d, prop_pie_d


if __name__ == '__main__':
    a, b = no_spending_by_bin()
    intended_spend(curr_pie_d=a, prop_pie_d=b)
