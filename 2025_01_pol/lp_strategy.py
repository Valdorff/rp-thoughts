import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd

# # price*/5_space2
# center_min_index = 0
# center_max_index = 3
# center_ls = [.0034 * 2**i for i in range(center_min_index, center_max_index + 1)]
# center_mult = 5

# # price*/2_space1.5
# center_min_index = 0
# center_max_index = 5
# center_ls = [.0034 * 1.5**i for i in range(center_min_index, center_max_index + 1)]
# center_mult = 2

# price*/3_space1.7 strategy
center_min_index = 0
center_max_index = 4
center_ls = [.0034 * 1.7**i for i in range(center_min_index, center_max_index + 1)]
center_mult = 3

c = list(mcolors.TABLEAU_COLORS)
print(c)

df = pd.read_csv('rpl_price_history.csv')
t_ls, price_ls = pd.to_datetime(df['datetime']), [x / 1e18 for x in df['rpl_price']]
pol_t_ls = []
pol_price_ls = []
pol_color_ls = []
pol_count_ls = []

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
        hi = price * center_mult
        lo = price / center_mult
        pol_count_ls.append(len([x for x in pol_price_ls if lo < x < hi]))
print(pol_count_ls)

fig, ax = plt.subplots(1)
ax.plot(t_ls, price_ls)
ax.scatter(pol_t_ls, pol_price_ls, color=pol_color_ls, marker='*')
ax.set_yscale('log')
for i in range(center_min_index, center_max_index + 1):
    center = center_ls[i]
    ax.axhline(center / center_mult, color=c[i], ls=':')
    ax.axhline(center * center_mult, color=c[i], ls='--')

# from counting "full range liquidity units"
# There are 1,774,544 ticks in a full range position
# There are 32,190 ticks in a price*/5 position; 55x more concentrated than full
# There are 21,973 ticks in a price*/3 position; 81x more concentrated than full
# There are 13,864 ticks in a price*/2 position; 128x more concentrated than full
# the "print(pol_count_ls)" line above can be used to generate a list of how many
# liquidity contributions were in range; these can be compared by multiplying with
# the appropriate concentration factors
fig2, ax2 = plt.subplots(1)
ax2.plot(range(1, 83 + 1), label='full_range')
ls5_2 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 58, 71, 60, 61, 62,
    63, 64, 65, 66, 67, 68, 69, 70, 71
]
ax2.plot([55 * x for x in ls5_2], label='price*/5_space2')
ls2_1p5 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 16, 21, 22, 19, 20, 21, 22,
    27, 28, 25, 26, 27, 28, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 39, 40, 41, 46, 47, 48, 49, 50,
    40, 52, 49, 54, 55, 45, 57, 47, 48, 49, 50, 36, 37, 38, 39, 40, 41, 42, 43, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 12, 13, 25, 15, 16
]
ax2.plot([128 * x for x in ls2_1p5], label='price*/2_space1.5')
ls3_1p7 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32, 33, 14, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 51, 52, 53, 54, 55, 56, 57, 58, 59, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 17, 48, 49, 50
]
ax2.plot([81 * x for x in ls3_1p7], label='price*/3_space1.7')
ax2.legend()

plt.show()
