import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    df = pd.read_csv('staking_snapshot_2.csv')
    df.groupby('withdrawal_address').agg(
        staked_rpl_value_in_eth=('staked_rpl_value_in_eth', np.sum),
        provided_eth=('provided_eth', np.sum),
        matched_eth=('matched_eth', np.sum),
        liquid_rpl_node_value_in_eth=('liquid_rpl_node_value_in_eth', np.sum),
        # use mean to avoid multiply counting rpl in the withdrawal address
        liquid_rpl_withdrawal_value_in_eth=('liquid_rpl_withdrawal_value_in_eth', np.mean),
    )
    df['neth_pct'] = df['staked_rpl_value_in_eth'] / df['provided_eth']
    df['liquid_rpl_value_in_eth'] = (
        df['liquid_rpl_node_value_in_eth'] + df['liquid_rpl_withdrawal_value_in_eth'])
    df['liquid_staked_proportion'] = df['liquid_rpl_value_in_eth'] / df['staked_rpl_value_in_eth']
    df = df[df['provided_eth'] > 0]

    fig, ax = plt.subplots(1)
    ax.scatter(df['neth_pct'], df['liquid_staked_proportion'], alpha=0.2)
    # noinspection PyTupleAssignmentBalance
    m, b = np.polyfit(df['neth_pct'], df['liquid_staked_proportion'], 1)
    ax.plot(df['neth_pct'], m * df['neth_pct'] + b, color='k', alpha=0.6)
    ax.set_xlabel('Staked RPL, as % bonded ETH')
    ax.set_ylabel(
        'liquid_rpl / effective_staked_rpl\n(liquid on node/withdrawal addresses or over 150%)')
    fig.savefig('./imgs/liquid_rpl.png', bbox_inches='tight')
    plt.show()

    # count number of active withdrawal addresses
    # convert portion over 1.5% to liquid
    # kde for various ranges (or maybe violins?)
    #   - 1.2-1.5
    #   - 0.9-1.2
    #   - 0.6-0.9
    #   - 0.3-0.6
    #   - 0.0-0.3

    # ax.violinplot(
    #     (df['knosh_pie'] / df['curr_pie']).dropna(),
    #     positions=[-200],
    #     widths=[250],
    #     showmedians=True,
    #     showextrema=False)

    # save off plots:
    #   - zoomed out
    #   - zoomed in 0-6.0
    #   - violins... for both? or maybe just zoomed


if __name__ == '__main__':
    main()
