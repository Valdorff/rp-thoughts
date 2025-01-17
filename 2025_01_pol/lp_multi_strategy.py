import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd

# Strategies will alternate each time

# strat = ['price*/5_space2', 'price*/2_space1.5']
# center_min_index = [0, 0]
# center_max_index = [3, 5]
# center_mult = [5, 2]
# space = [2, 1.5]
# concentration_mult = [55, 128]

strat = ['price*/5_space2', 'price*/1.6_space1.5']
center_min_index = [0, 0]
center_max_index = [3, 5]
center_mult = [5, 1.6]
space = [2, 1.5]
concentration_mult = [55, 377.6]

# from counting "full range liquidity units"
# There are 1,774,544 ticks in a full range position
# There are 32,190 ticks in a price*/5 position; 55x more concentrated than full
# There are 21,973 ticks in a price*/3 position; 81x more concentrated than full
# There are 13,864 ticks in a price*/2 position; 128x more concentrated than full
# There are 4,400 ticks in a price*/1.6 position; 377.6x more concentrated than full

c = list(mcolors.TABLEAU_COLORS)
mrk = '*osPXD'

df = pd.read_csv('rpl_price_history.csv')
t_ls, price_ls = pd.to_datetime(df['datetime']), [x / 1e18 for x in df['rpl_price']]
pol_t_ls = [[] for _ in range(len(strat))]
pol_price_ls = [[] for _ in range(len(strat))]
pol_color_ls = [[] for _ in range(len(strat))]
pol_count_ls = []  # this is net across strategies

last_delta = None
for t, price in zip(t_ls, price_ls):
    delta = (t - t_ls[0]).days
    if delta == last_delta:  # avoid double counting with multiple price submissions in one day
        continue
    else:
        last_delta = delta

    if (delta % 14 == 0) and (delta > 20):
        strat_ind = len(pol_count_ls) % len(strat)
        center_ls = [
            .0034 * space[strat_ind]**i
            for i in range(center_min_index[strat_ind], center_max_index[strat_ind] + 1)
        ]
        pol_t_ls[strat_ind].append(t)
        closest_ind = min(range(len(center_ls)), key=lambda i: abs(center_ls[i] - price))
        pol_price_ls[strat_ind].append(center_ls[closest_ind])
        pol_color_ls[strat_ind].append(c[closest_ind])
        count = 0
        for i in range(len(strat)):
            hi = price * center_mult[i]
            lo = price / center_mult[i]
            count += concentration_mult[i] * len([x for x in pol_price_ls[i] if lo < x < hi])
        pol_count_ls.append(count)
print(pol_count_ls)

fig, ax = plt.subplots(1)
ax.plot(t_ls, price_ls)
for i in range(len(strat)):
    ax.scatter(pol_t_ls[i], pol_price_ls[i], color=pol_color_ls[i], marker=mrk[i], label=strat[i])
ax.set_yscale('log')
for strat_ind in range(len(strat)):
    for i in range(center_min_index[strat_ind], center_max_index[strat_ind] + 1):
        center_ls = [
            .0034 * space[strat_ind]**i
            for i in range(center_min_index[strat_ind], center_max_index[strat_ind] + 1)
        ]
        center = center_ls[i]
        xmin = strat_ind / len(center_mult)
        xmax = (strat_ind + 1) / len(center_mult)
        ax.axhline(center / center_mult[strat_ind], color=c[i], ls=':', xmin=xmin, xmax=xmax)
        ax.axhline(center * center_mult[strat_ind], color=c[i], ls='--', xmin=xmin, xmax=xmax)
ax.legend()

# the "print(pol_count_ls)" line above can be used to generate a list of how many equivalent units
# of liquidity contributions were in range
fig2, ax2 = plt.subplots(1)
# ax2.plot(range(1, 83 + 1), label='full_range')
# multi_5_2__2_1p5 = [
#     55, 183, 238, 366, 421, 549, 604, 732, 787, 915, 970, 1098, 1153, 1281, 1336, 1464, 1519, 1647,
#     1702, 1574, 1885, 2013, 1812, 1940, 1995, 2123, 2434, 2562, 2361, 2489, 2544, 2672, 1703, 1831,
#     1886, 2014, 2069, 2197, 2252, 2380, 2435, 2563, 3642, 3770, 3825, 4209, 4264, 4392, 4447, 4575,
#     3862, 4758, 4557, 4941, 4996, 4356, 5179, 4539, 4594, 4722, 4777, 4009, 4064, 4192, 4247, 4375,
#     4430, 4558, 4613, 2491, 2876, 2674, 2729, 2857, 2912, 3040, 3095, 3223, 2638, 2766, 3461, 2949,
#     3004
# ]
# ax2.plot(multi_5_2__2_1p5, label='price*/5_space2, price*/2_space1.5')
multi_5_2__1p6_1p5 = [
    55.0, 432.6, 487.6, 865.2, 920.2, 1297.8000000000002, 1352.8000000000002, 1730.4, 1785.4,
    2163.0, 2218.0, 2595.6000000000004, 2650.6000000000004, 3028.2000000000003, 3083.2000000000003,
    3460.8, 3515.8, 3893.4, 3948.4, 3570.8, 3625.8, 4003.4, 4058.4, 1792.8000000000002, 4491.0,
    4868.6, 5678.8, 5301.200000000001, 5356.200000000001, 5733.8, 5788.8, 3145.6000000000004,
    3200.6000000000004, 1690.2, 3633.2000000000003, 4010.8, 4065.8, 4443.4, 4498.4, 4876.0, 4931.0,
    5308.6, 5363.6, 5741.200000000001, 8817.0, 6929.0, 6984.0, 7361.6, 7416.6, 7794.200000000001,
    8604.400000000001, 8226.8, 8281.8, 8659.400000000001, 8714.400000000001, 9092.0, 9147.0,
    10279.800000000001, 10334.800000000001, 10712.400000000001, 8124.200000000001, 8501.8, 8556.8,
    3270.4, 3325.4, 3703.0, 3758.0, 4135.6, 4190.6, 4238.200000000001, 4623.200000000001, 2782.8,
    2837.8, 3215.4, 3270.4, 3648.0, 3703.0, 4080.6000000000004, 4135.6, 2247.6, 4568.200000000001,
    4945.8, 5000.8
]
ax2.plot(multi_5_2__1p6_1p5, label='price*/5_space2, price*/1.6_space1.5')

ls5_2 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 58, 71, 60, 61, 62,
    63, 64, 65, 66, 67, 68, 69, 70, 71
]
ax2.plot([55 * x for x in ls5_2], label='price*/5_space2')
# ls2_1p5 = [
#     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 16, 21, 22, 19, 20, 21, 22,
#     27, 28, 25, 26, 27, 28, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 39, 40, 41, 46, 47, 48, 49, 50,
#     40, 52, 49, 54, 55, 45, 57, 47, 48, 49, 50, 36, 37, 38, 39, 40, 41, 42, 43, 14, 15, 16, 17, 18,
#     19, 20, 21, 22, 12, 13, 25, 15, 16
# ]
# ax2.plot([128 * x for x in ls2_1p5], label='price*/2_space1.5')
ax2.legend()

plt.show()
