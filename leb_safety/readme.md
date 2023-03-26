# [DRAFT] Risk analyis for LEBs
March 2023

## Abstract

Previous work has looked into the amount of bond that's necessary for safety assuming various
malicious behaviors and assuming various available mitigations. See for example,
[Ken Smith's work](https://github.com/htimsk/LEBminipools) and 
[Stader's ETHx Litepaper](https://www.staderlabs.com/docs/eth/Stader%20ETH%20Litepaper.pdf).

Both of these analyses dramatically underestimate the potential for loss because they assume that
the market they've been able to sample is truly representative of the future market. I will show
that we already have strong evidence that the MEV market varies significantly over time. I will use
that understanding to estimate some "clearly" unsafe bond levels.

## Types of losses
- Correlated slashing
- Slashing and leakage
- Execution layer reward theft - continuous
- Execution layer reward theft - large block

## Analyzing each type of loss

### Correlated slashing
We can ignore this term. No RP user should be able to cause this themselves, and if they can there's
no reason to believe they could do so at all profitably.

### Slashing and leakage
From a game theory standpoint, an adversary "should" slash themselves if they have no remaining
stake. They would then allow leakage on their way out. This increases the cost to the protocol of
kicking them without incurring any cost on their end. We will ignore this term as any situation
that's considered "safe" relies on the NO having _some_ stake left.

### Execution layer reward theft - continuous
As of when I'm writing, MEV makes for very roughly 2% APR. We see from the data that about 18% of
MEV is below the median, so we can use that as a reasonable estimate of what we can expect from
continuous theft for one validator. Something like 0.0036%, or 0.115 ETH/year.

![](./imgs/value_above_median.png)

However, if an adversary has a large number of validators stealing continuously, it becomes more
appropriate to use the average APR of 2% instead of the median. In that case, we are losing ~0.64ETH
per validator per year.

This variable must be considered if we're not able to execute on forced exits. Essentially, if we
want a 5-year buffer and don't have forced exits, we'd want to buffer by .64*5 = 3.2 ETH _beyond_
the ETH directly used to counteract a large block theft.

### Exeution layer reward theft - large block
This plot shows the percent of blocks above a specific percentile. The key takeaway is that the
market is not (at all) the same every week. There is no particular reason to expect we've seen
anything remotely like the bounds of what the MEV market can look like. One could speculatively
argue that MEV will be much higher during a bull market or once incredibly-valuable layer2 commit
transactions are commonplace. There are arguments for a reducing impact of MEV as well, but we must
plan for the worst case.

We have had 3 "high-execution-reward" weeks so far, out of 29. Over 10% is quite common. For the
following analysis, I'll assume we need to defend against an MEV market that looks like that all the
time. I consider this a bad case, but not at all pushing the amounts we could speculate the market
reaches.

![](./imgs/lotto_blocks.png)

**LEB8s without forced exits:** During such a period, the 99.9th percentile block is ~9 ETH.
Combined with the current ~77 days per proposal, this would mean one out of 11k minipools would
profit from stealing each week at that level (ignoring the RPL bond). If the market acts like this
for a year, roughly 1 in 200 minipools would profit from stealing. While the 2.4 ETH minimum RPL
bond gets us back to a "safe" level, it only does so by 1.4 ETH, which is 2 years of continous
theft.

**LEB4s without forced exits:** During such as period, the 99.7th percentile block is just over 4
ETH. This would mean roughly one out of 3700 minipools would profit from stealing each week. If the
market acts like this for a year, roughly 1 in 70 minipools would profit from stealing. A 2.8 ETH
bond would get us to a safe level for ~4 years.

**LEB4s with forced exits:** During such a period, the 99.83rd percentile block is just over 6.8
ETH. This would mean roughly one out of 6500 minipools would profit from stealing each week. If the
market acts like this for a year, roughly 1 in 120 minipools would profit from stealing.

## Conclusions
### Minipool loss
So - what would the damage be? After a year with the market looking like that, assuming everyone is
purely maximizing profit and sybil attacking to the max (implies minimum RPL bond too), we'd see
~.5% of LEB8s without forced exits steal, ~1.4% of LEB4s without forced exits steal, and ~.8% of
LEB4s with forced exits steal. These minipools become a drain to RP. If forced exits exist, they are
exited; if not, they stick around stealing MEV.

### Value loss
Here we see a chart showing the value above a specific percentile. We don't
see great correlation, but it looks like when we have bigger lotto blocks they are more of the
total value (ie, the increase in the lotto blocks outweighs any increase in common blocks).

![](./imgs/value_in_lotto_blocks.png)

Looking at all time, we'd expect to lose ~16% of execution layer rewards to large block theft.
Looking at just the big lotto block weeks (2, 10, 27), we'd expect to lose about 22% of execution
layer rewards to large block theft. 

Execution layer rewards are around 1/3 of total rewards, so this would cause a loss of 5.3%/7.3%
respectively. This is quite significant -- eg, compare with our 15% commission or the deposit pool,
which we try to keep to a max of 5% drag.

If we have no forced exits, we would also suffer the loss of execution rewards going forward, but
it's a smaller effect than the large block theft damage. We'd see .005/3 = .17% for LEB8s, or
.008/3 = .27% for LEB4s. Unlike the large block theft term, it should be noted that if the market
continues this way for many years, it would continue accruing - eg, after 2 years we'd be at
.34%/.54% respectively for LEB8s/LEB4s.

### It could be worse
Remember, I'm using something like the worst 10% we've seen as a model. It's _entirely possible_
that the market leaves the range we've seen entirely.

I'll also note that I'm looking at just one relay here. Looking at more will certainly show more
chances for lottery blocks, though I can't quantify by how much.

## Mitigation

### Node-level collateral
Large block theft relies on abusing events that are rare per validator and random. This means that a
strong defense would be to penalize at the node level. For example, if you have 2 LEB4s with 2.8 ETH
worth of RPL, the total bond is actually 13.6 ETH if we're able to penalize at the node level. This
would require somewhat more complex code to determine safe cutoffs, but it would mitigate the attack
an arbitrary amount. A downside is that it would also prevent RP from serving small operators that
can only afford the bond for one small minipool.

### Assign MEV to NOs
This variant avoids the theft concept entirely by assigning it to NOs. The NOs would be responsible
for paying an average MEV fee each period to prevent rETH from losing out.

A rough implementation outline:
- Use smoothing pool or other large sample to calculate average MEV for reward period X
- This value is recorded on-chain
- When claiming from a minipool, calculate the ETH owed from each reward period that has passed
  since last claim (taking commission into account) and store that debt in a variable on the
  minipool
- Distributions go entirely to rETH until that debt is repaid 
- Additional ETH to be distributed is paid out normally (split between NO and rETH holder)

There may be small optimizations available, like skipping this process for continuous smoothing
pool participants.

The negative here is a difficult-to-calculate number that would probably need to be done using an
off-chain oracle.