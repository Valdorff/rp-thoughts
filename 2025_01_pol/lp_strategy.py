from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

# current price*/5 strategy
center_min_index = 0
center_max_index = 3
center_ls = [.0034 * 2**i for i in range(center_min_index, center_max_index + 1)]
center_mult = 5

# # proposed price*/2 strategy
# center_min_index = 0
# center_max_index = 5
# center_ls = [.0034 * 1.5**i for i in range(center_min_index, center_max_index + 1)]
# center_mult = 2

c = list('rgbcmyk')

df = pd.read_csv('rpl_price_history.csv')
t_ls, price_ls = pd.to_datetime(df['datetime']), [x / 1e18 for x in df['rpl_price']]
pol_t_ls = []
pol_price_ls = []
pol_color_ls = []

last_delta = None
for t, price in zip(t_ls, price_ls):
    delta = (t - t_ls[0]).days
    if delta == last_delta:  # avoid double counting with multiple price submissions in one day
        continue
    else:
        last_delta = delta
    if (delta % 14 == 0) and (delta > 20):
        pol_t_ls.append(t)
        closest_ind = min(range(len(center_ls)), key=lambda i: abs(center_ls[i] - price))
        pol_price_ls.append(center_ls[closest_ind])
        pol_color_ls.append(c[closest_ind])

fig, ax = plt.subplots(1)
ax.plot(t_ls, price_ls)
ax.scatter(pol_t_ls, pol_price_ls, color=pol_color_ls, marker='*')
ax.set_yscale('log')
for i in range(center_min_index, center_max_index + 1):
    center = center_ls[i]
    ax.axhline(center / center_mult, color=c[i], ls=':')
    ax.axhline(center * center_mult, color=c[i], ls='--')
plt.show()
