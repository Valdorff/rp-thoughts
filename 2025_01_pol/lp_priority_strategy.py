import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd

# will use the earliest strategy until condition is met

# Get some concentrated liquidity up first, then slowly build up wide liquidity
strat = ['price*/1.6_space1.5', 'price*/5_space2']
center_min_index = [0, 0]
center_max_index = [5, 3]
center_mult = [1.6, 5]
space = [1.5, 2]
concentration_mult = [377.6, 55]
strat_count = [3, 9999]  # No. of times a strategy is used at a level before using next strategy

# # Get some foundation wide liquidity up first, then build up concentrated liquidity, then back wide
# strat = ['price*/1.6_space1.5', 'price*/5_space2', 'price*/1.6_space1.5', 'price*/5_space2']
# center_min_index = [0, 0, 0, 0]
# center_max_index = [5, 3, 5, 3]
# center_mult = [1.6, 5, 1.6, 5]
# space = [1.5, 2, 1.5, 2]
# concentration_mult = [377.6, 55, 377.6, 55]
# strat_count = [2, 2, 3,
#                9999]  # No. of times a strategy is used at a level before using next strategy

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
        for strat_ind in range(len(strat)):
            center_ls = [
                .0034 * space[strat_ind]**i
                for i in range(center_min_index[strat_ind], center_max_index[strat_ind] + 1)
            ]
            closest_ind = min(range(len(center_ls)), key=lambda i: abs(center_ls[i] - price))
            if pol_price_ls[strat_ind].count(center_ls[closest_ind]) >= strat_count[strat_ind]:
                continue  # go to next strat
            pol_t_ls[strat_ind].append(t)
            pol_price_ls[strat_ind].append(center_ls[closest_ind])
            pol_color_ls[strat_ind].append(c[closest_ind])
            break  # strat worked, stop searching
        count = 0
        for i in range(len(strat)):
            hi = price * center_mult[i]
            lo = price / center_mult[i]
            count += concentration_mult[i] * len([x for x in pol_price_ls[i] if lo < x < hi])
        pol_count_ls.append(count)

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

# ax2.plot(pol_count_ls, label='live_run')

prio3_1p6_1p5__5_2 = [
    377.6, 755.2, 1132.8000000000002, 1187.8000000000002, 1242.8000000000002, 1297.8000000000002,
    1352.8000000000002, 1407.8000000000002, 1462.8000000000002, 1517.8000000000002,
    1572.8000000000002, 1627.8000000000002, 1682.8000000000002, 2060.4, 2438.0, 2815.6000000000004,
    2870.6000000000004, 2925.6000000000004, 2980.6000000000004, 2225.4, 2280.4, 2658.0,
    3035.6000000000004, 1957.8000000000002, 3145.6000000000004, 3200.6000000000004, 4388.4,
    3310.6000000000004, 3365.6000000000004, 3420.6000000000004, 3475.6000000000004, 2720.4, 3098.0,
    2342.8, 3530.6000000000004, 3585.6000000000004, 3640.6000000000004, 3695.6000000000004,
    3750.6000000000004, 3805.6000000000004, 3860.6000000000004, 3915.6000000000004,
    3970.6000000000004, 4025.6000000000004, 5213.4, 4135.6, 4190.6, 4245.6, 4300.6, 4355.6, 5543.4,
    4465.6, 4520.6, 4575.6, 4630.6, 4685.6, 4740.6, 5928.4, 5983.4, 6038.4, 4960.6, 5015.6, 5070.6,
    3992.8, 4047.8, 4102.8, 4480.4, 4858.0, 4913.0, 4795.6, 5345.6, 3772.8, 4150.4, 4205.4, 4260.4,
    4315.4, 4370.4, 4425.4, 4803.0, 4047.8, 5235.6, 5290.6, 5345.6
]
ax2.plot(prio3_1p6_1p5__5_2, label='prio3: price*/1.6_space1.5, price*/5_space2')

# prio5_1p6_1p5__5_2 = [
#     377.6, 755.2, 1132.8000000000002, 1510.4, 1888.0, 1943.0, 1998.0, 2053.0, 2108.0, 2163.0,
#     2218.0, 2273.0, 2328.0, 2705.6000000000004, 3083.2000000000003, 3460.8, 3838.4, 3893.4, 3948.4,
#     2815.6000000000004, 2870.6000000000004, 3248.2000000000003, 3625.8, 2115.4, 4381.0, 4436.0,
#     6001.400000000001, 4546.0, 4601.0, 4656.0, 4711.0, 3200.6000000000004, 3578.2000000000003,
#     2067.8, 4333.4, 4711.0, 4766.0, 4821.0, 4876.0, 4931.0, 4986.0, 5041.0, 5096.0, 5151.0, 7094.0,
#     5261.0, 5316.0, 5371.0, 5426.0, 5481.0, 7046.400000000001, 5591.0, 5646.0, 5701.0, 5756.0,
#     5811.0, 5866.0, 7431.400000000001, 7486.400000000001, 7541.400000000001, 6031.0, 6086.0, 6141.0,
#     4308.0, 4363.0, 4418.0, 4795.6, 5173.200000000001, 5228.200000000001, 5220.8, 5983.4, 4088.0,
#     4465.6, 4520.6, 4575.6, 4630.6, 4685.6, 4740.6, 5118.200000000001, 3607.8, 5550.8, 5928.4,
#     6306.0
# ]
# ax2.plot(prio5_1p6_1p5__5_2, label='prio5: price*/1.6_space1.5, price*/5_space2')

ls5_2 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 58, 71, 60, 61, 62,
    63, 64, 65, 66, 67, 68, 69, 70, 71
]
ax2.plot([55 * x for x in ls5_2], label='price*/5_space2')
ax2.legend()

plt.show()
