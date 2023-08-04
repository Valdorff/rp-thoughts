import matplotlib.pyplot as plt
import numpy as np


def current_intended_spend():
    # Looking at intervals 12-14
    # Data from https://docs.google.com/spreadsheets/d/1jA51myEsuqxhdJyYaBmFvt4RR5RVluPjk1Wl8OCt8Uw/edit#gid=0
    # but used 34.1% for IMC and 20.5% for GMC to align with intent

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
    print(pie_weights)
    pie_labels = ['NOs', 'Dev', 'oDAO (non-dev)', 'IMC', 'GMC', 'Reserves (non-dev)']
    ax.pie(pie_weights, labels=pie_labels, autopct='%1.1f%%', pctdistance=.85)
    fig.savefig('./imgs/overall_spend_pie.png', bbox_inches='tight')

    plt.show()


if __name__ == '__main__':
    current_intended_spend()
