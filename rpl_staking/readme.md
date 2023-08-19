# RPL Staking Rework Proposal
August 2023

## Summary
### Goals
- Concentrate spend on RP goals, particularly incentivizing NOs to create rETH supply by
  - rewarding making more minipools
  - rewarding LEB8s more than EB16s
- Avoid spend that doesn't support RP goals, particularly unneccessarily rewarding speculation
- Folks shouldn't feel trapped - some exit friction is ok... predictable is good, and we shouldn't
  be extortionate
- Folks shouldn't feel they have to actively modify allocations for every little ratio change

### Proposed changes
- Rewards will scale differently (see [details below](#the-actual-reward-math) for the math)
  - Adding a minipool will increase RPL rewards (even if you already had enough staked RPL)
    **[new]**
  - Converting an EB16 to two LEB8s will increase rewards (even if you already had enough staked RPL)
    **[new]**
  - You need staked RPL value of ≥10% borrowed ETH to get RPL rewards **[unchanged]**
  - Staking more RPL means more rewards **[unchanged]**, now without a maximum **[new]**
  - Beyond 15% borrowed ETH, additional rewards go up slower and slower **[new]**
- The minimum to withdraw will be 15% borrowed ETH
- Make withdrawal a 2-step process
  - Set X RPL to "withdrawing"; these RPL are no longer eligible for rewards or voting
  - After a time period (make a setting; start it at 28 days), the RPL may be withdrawn
  - (Remove the current withdrawal lock when you stake RPL)
- Phase in the new rules slowly over 6 months (see [details below](#phasing-in-the-rules))
- These changes apply equally to both existing and new NOs

## Context
### How RP currently spends inflation revenue
| ![image](./imgs/overall_spend_bar.png) |   ![image](./imgs/overall_spend_pie.png)   |
|:--------------------------------------:|:-----------------------------------:|

As we can see - our spend on NOs is enormous -- it's _really important_ that we make it count. \
A year of inflation is about 981k RPL, with 687k going to NOs. At the current price of $28, that's
$19.2M per year going to NOs.

### How RP currently spends inflation revenue; with NO rewards categorized
| ![image](./imgs/overall_spend_pie_curr.png) | ![image](./imgs/overall_spend_pie_prop.png) |
|:-------------------------------------------:|:-------------------------------------------:|

The proposal focuses a _lot_ more spend on incentivizing minipool creation, while still spending a
significant amount on the speculative and hands-off categories of RPL staking (compare with Dev
spend, for example). The current outsized speculation category (larger than Dev, oDAO, IMC, GMC, and
Reserves _combined_) has been significantly reduced so that we can spend a lot more on achieving the
protocol goal of attracting minipool creation (and rETH supplying).

For a step-by-step breakdown, look [in the detail section](#how-rp-currently-spends-no-rewards).

## What does this mean for me?
In the long run, people might change allocations, so it's not an easy answer, but we can look at
what it means _immediately_. 
- Currently, the only folks that would go down in rewards are folks with EB16s and very high staked
  RPL. This makes sense given the goal of incentivizing rETH supply.
- The folks that win the most are those at the low end of staked RPL staked on LEB8s. This makes
  sense because these folks are a little hesitant; we're using greater rewards to convince them to
  join and/or make more minipools.
- You can check out the plots below to get a feel for the impact in your case
- For full detail, there's a simulator at https://www.desmos.com/calculator/b5gdrnwowc
  - Ignore the graph component - no way to hide it, but we won't be using it
  - You enter the number of 8/16 ETH minipools (as m8 and m16 respectively) 
  - You enter the value of staked RPL in ETH as r (note that you can enter an expression like
    `300*.015` if you know your amount of RPL and the ratio instead) 
  - You read off your share of the pie (in millionths) on line 10 for the current structure and
    line 12 for the proposed structure
  - You read off the advantage of the proposal on line 14 (2 means you get double the rewards, 0.5
    means you get half the rewards, etc.)
- Note: since the calculations are based on the amount of borrowed ETH and staked RPL, there's no
  way to use splitting across multiple nodes to get more rewards

### Plots of rewards and APR per pool

The plots on the left show the rewards for a single minipool based on amount of staked RPL.

The plots on the right show what that means in terms of marginal APR - in other words, if you have x
ETH worth of RPL staked and stake a tiny bit more, how much yield will you get on that tiny bit.

All of these plots are based on a recent snapshot of staked RPL.

![image](./imgs/rewards_summary.png)

### Plots comparing current and proposed rewards 
The plot below on the left shows the rewards for a single minipool based on amount of staked RPL.

The plot on the right shows the difference for those same minipools under the two systems.

Both of these plots are based on a recent snapshot of staked RPL.

| ![image](./imgs/rule_pc.png) | ![image](./imgs/rulediff_pc.png) |
|:----------------------------:|:--------------------------------:|

#### Reading the difference plot (the one on the right)
Scenario 1: You have 4 LEB8s and 20 ETH worth of RPL staked
- That's 5 ETH worth per LEB8
- Look at the 5 on the x-axis and find where that crosses the solid LEB8 line
- Just over 200% - a big RPL yield win for this NO!

Scenario 2: You have 2 EB16s and 20 ETH worth of RPL staked
- That's 10 ETH worth per EB16
- Look at the 10 on the x-axis and find where it crosses the dashed EB16 line
- Around 80% - a moderate yield loss for this NO... maybe it's time to consider swapping to LEB8s?
- You can get further detail by using the [simulator](https://www.desmos.com/calculator/b5gdrnwowc)
  mentioned above
  - Input m8=0, m16=2, r=20. You see that under the current system you receive 126.5ppm of the net
    NO rewards, and with the proposed system you'd be at 105.9ppm
  - But what if we swapped to LEB8s? Input m8=4, m16=0, r=20. You see that under the current system
    you'd receive 126.5ppm, and with the proposed system you'd be at 262.9ppm! Definitely makes it
    faster to pay back the idle time in the validator queue :)

## Details
### The actual reward math
Rewards will be based on weight
- If your staked RPL value in ETH is below 10% borrowed ETH, weight is 0
- From 10%-15% borrowed ETH, weight is linear with the amount of borrowed ETH
  - 🧮 `weight = 100 * staked_rpl_value_in_eth`
- Above 15%, weight follows a logarithmic curve, rising forever, but ever-more-slowly
  - 🧮 `weight = (13.6137 + 2 * ln(100 * (staked_rpl_value_in_eth / borrowed_eth) - 13)) * borrowed_eth`
- The NO share of inflation gets split up to each node as `weight/total_summed_weight`

### Phasing in the rules
For rewards, this can be achieved by calculating the "share of the pie" for both rule sets, and then
adding them together in a changing proportion.
- Period X after the vote: `0.17*x*proposed_share + 0.17*(6-x)*current_share`  
- After period 5, simply used proposed_share

For the withdrawal threshold, it's a little complicated. First, it requires a pDAO guardian action,
so we don't want to do a ton of changes. Second, the current setting is based off of bonded ETH,
_not_ borrowed ETH. This means 16-ETH minipool holders will have a higher withdrawal threshold than
intended. Still, it will be much lower than the current one (less than a third).
- After Period X=3 rewards go out, set withdrawal threshold to 100% bonded ETH
- After Period X=6 rewards go out, set withdrawal threshold to 60% bonded ETH
  - This is 20% borrowed ETH for LEB8s (close to the desired 15%, but with some buffer);
    unfortunately, it's 60% borrowed ETH for 16-ETH minipools (much higher than the desired 15%),
    but that's the best we can do without a SC change
- In the next planned Smart Contract release, update to:
  - have 2-step withdrawals w/28 day withdrawing time
  - be based on borrowed ETH w/15% borrowed ETH threshold

### How RP currently spends NO rewards
Let's start by looking at what staked RPL we reward:

| ![image](./imgs/no_bar_bins_curr.png) |  ![image](./imgs/no_bar_bins_prop.png) |
|:------------------------------------:|:------------------------------------:|

As we can see, we spend progressively less on each increasingly higher "bin" of RPL. For the current
setup, this comes about because you can't have the 20-25% bin full without having the 15-20% bin
full. For the proposed setup, that's still true AND rewards per RPL decrease as you go higher up, so
we are more concentrated in the lowest bins. Note that the bins have been color-coded into 3
categories: the lowest bin directly incentivizes minipool creation, a few bins after that allow for
some overshoot with RPL growth (this is partly speculation and partly NOs taking a hands-off
approach), and bins beyond that are quite speculative. Let's take a look at what the totals in those
categories are:

| ![image](./imgs/no_pie_bins_curr.png) | ![image](./imgs/no_pie_bins_prop.png) |
|:-------------------------------------:|:-------------------------------------:|

Here we see that the proposal significantly concentrates the NO reward spend towards incentivizing
new minipools. Let's put that in the context of our total spend:

| ![image](./imgs/overall_spend_pie_curr.png) | ![image](./imgs/overall_spend_pie_prop.png) |
|:-------------------------------------------:|:-------------------------------------------:|

The proposal focuses a lot more spend on incentivizing minipool creation, while still spending a
significant amount on the speculative and hands-off categories of RPL staking (compare with Dev
spend, for example). The current outsized speculation category (larger than Dev, oDAO, IMC, GMC, and
Reserves combined) has been significantly reduced so that we can spend a lot more on achieving the
protocol goal of attracting minipool creation (and rETH supplying).

### What else has been looked at around this proposal?
- There was a very active [discord
  thread](https://discord.com/channels/405159462932971535/1129516706323234916/1129516793279549505)
  for about 3 weeks starting on 2023-07-14
- The discord thread was kicked off with a research document that evolved along with the active
  discussion. You can check out the latest version of that document [here](./research.md).
  - The initial proposal got a number of tweaks based on community feedback in this process
    (shoutout to the many people that participated in discussion - this community is the bomb!) 
  - One aspect that got a lot of attention was the potential for damage to RPL price, especially
    self-reinforcing damage. No convincing trigger for this RPL price damage was suggested beyond
    narrative fear/uncertainty/doubt. The research document has a section that shows the _small_
    portion of RPL that might potentially be rationally sensitive to the proposed change in rewards.
- Pieter wrote a [steelman argument](https://hackmd.io/@pieterastra/HkpTLBhqh) against the proposal
  based on personas
  - I responded in [discord](https://discord.com/channels/405159462932971535/1129516706323234916/1134193421100257331),
    and the high level conclusion bullets bear highlighting, imo:
    1. I acknowledge there are real, potentially large, risks involved with change
    1. I believe there are also real, potentially large, risks involved with refusal to change
    1. As such, I don't think our mainline choices should be driven by either of those. I do think
      it's critical to think about how to minimize those risks (making things digestible, talking to
      achieve significant consensus, ramping things in, etc, etc).
- Despite repeatedly asking for a model showing that rational actors would sell significantly, no
  such model was ever presented. One self-quote on that front:
    > Yes. But let's be very clear that we do have at least my prediction about what will happen,
    which knoshua contributed to as well.
    > 
    > So I'd like to see a model on a similar level take the other side. If we can only make
    realistic models show no big sell-off and have to resort to "well anything is possible" to
    show a big sell-off... That's got weight to it too.
    > 
    > [Three community members] have all presented possible scenarios and explicitly flagged them
    as things you don't consider likely, or aren't predicting. 🤷‍♂️
  