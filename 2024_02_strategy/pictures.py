import matplotlib.pyplot as plt


def eth_only_roi(n_minipools, commission):
    bonded = 0
    borrowed = 0
    aggro_ls = []
    aggro_bonded = []
    for i in range(n_minipools):
        if i < 1:
            bonded += 6
            borrowed += 26
        else:
            bonded += 1.5
            borrowed += 30.5
        aggro_ls.append((bonded + commission * borrowed) / bonded)
        aggro_bonded.append(bonded)

    bonded = 0
    borrowed = 0
    aggroalt_ls = []
    aggroalt_bonded = []
    for i in range(n_minipools):
        if i < 2:
            bonded += 4
            borrowed += 28
        else:
            bonded += 1.5
            borrowed += 30.5
        aggroalt_ls.append((bonded + commission * borrowed) / bonded)
        aggroalt_bonded.append(bonded)

    bonded = 0
    borrowed = 0
    safer_ls = []
    safer_bonded = []
    for i in range(n_minipools):
        if i < 6:
            bonded += 4
            borrowed += 28
        else:
            bonded += 2
            borrowed += 30
        safer_ls.append((bonded + commission * borrowed) / bonded)
        safer_bonded.append(bonded)

    x = list(range(1, n_minipools + 1))
    fig, (ax0, ax1) = plt.subplots(2)
    # ax0.plot(x, aggro_ls, label='Aggressive')
    # ax0.plot(x, safer_ls, label='A bit safer')
    ax0.plot(x, aggroalt_ls, label='Aggressive [alt]', color='#FD7861')
    ax0.axhline(
        (1.5 + commission * 30.5) / 1.5, color='#FD7861', alpha=0.8, ls=':', label='asymptote')
    ax0.axhline(1.5, color='#00A3FF', alpha=0.8, ls='--', label='Lido CSM')
    ax0.set_xlabel('Minipool Count')
    ax0.set_ylabel('ROI in units of solo apr')
    ax0.grid()
    ax0.legend()
    # ax1.plot(aggro_bonded, aggro_ls, label='Aggressive')
    # ax1.plot(safer_bonded, safer_ls, label='A bit safer')
    ax1.plot(aggroalt_bonded, aggroalt_ls, color='#FD7861', label='Aggressive [alt]')
    ax1.axhline(
        (1.5 + commission * 30.5) / 1.5, color='#FD7861', alpha=0.8, ls=':', label='asymptote')
    ax1.axhline(1.5, color='#00A3FF', alpha=0.8, ls='--', label='Lido CSM')
    ax1.set_xlabel('Bonded ETH')
    ax1.set_ylabel('ROI in units of solo apr')
    ax1.grid()
    ax1.legend()
    fig.tight_layout()
    fig.savefig('eth_only_roi.png')


def eth_revenue_pies():
    currsizes = [86, 14]
    currlabels = ['rETH', 'RPL-staking NOs']
    currcolors = ['#FD7861', '#FFD48A']

    propsizes = [86, 9, 5]
    proplabels = ['rETH', 'RPL stakers', 'NOs']
    propcolors = ['#FD7861', '#FFD48A', '#888888']

    fig, (ax0, ax1) = plt.subplots(1, 2)
    ax0.pie(currsizes, labels=currlabels, colors=currcolors, autopct='%1.1f%%')
    ax0.set_xlabel('Current Split')
    ax1.pie(propsizes, labels=proplabels, colors=propcolors, autopct='%1.1f%%')
    ax1.set_xlabel('Proposed Split')
    fig.tight_layout()
    fig.savefig('eth_revenue_pies.png', bbox_inches='tight', pad_inches=0.2)


if __name__ == '__main__':
    eth_only_roi(n_minipools=60, commission=.05)
    eth_revenue_pies()
    plt.show()
