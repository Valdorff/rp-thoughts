import matplotlib.pyplot as plt
n = 50
commission = .14
# commission = .14 * .35

bonded = 0
borrowed = 0
aggro_ls = []
for i in range(n):
    if i <= 1:
        bonded += 6
        borrowed += 26
    else:
        bonded += 1.5
        borrowed += 30.5
    aggro_ls.append((bonded + commission * borrowed) / bonded)

bonded = 0
borrowed = 0
aggroalt_ls = []
for i in range(n):
    if i <= 2:
        bonded += 4
        borrowed += 28
    else:
        bonded += 1.5
        borrowed += 30.5
    aggroalt_ls.append((bonded + commission * borrowed) / bonded)

bonded = 0
borrowed = 0
safer_ls = []
for i in range(n):
    if i <= 6:
        bonded += 4
        borrowed += 28
    else:
        bonded += 2
        borrowed += 30
    safer_ls.append((bonded + commission * borrowed) / bonded)

x = list(range(1, n + 1))
fig, ax = plt.subplots(1)
ax.plot(x, aggro_ls, label='Aggressive')
ax.plot(x, aggroalt_ls, label='Aggressive [alt]')
ax.plot(x, safer_ls, label='A bit safer')
ax.axhline((1.5 + commission * 30.5) / 1.5, color='k', alpha=0.8, ls=':')
ax.axhline((2 + commission * 30) / 2, color='k', alpha=0.8, ls=':')
ax.set_xlabel('Minipool Count')
ax.set_ylabel('ROI in units of solo apr')
ax.grid()
ax.legend()
plt.show()
