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
that understanding to estimate some "clearly" unsafe bond levels. I will assume the availability of
forced exits.

## Types of losses
- Correlated slashing
- Slashing and leakage
- Execution layer reward theft - continuous
- Execution layer reward theft - large block

## Analyzing the easier terms

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
continuous theft. Something like 0.0036%, or 0.115 ETH/year.

![](./imgs/value_above_median.png)



## Mitigation
- Enough collateral across multiple nodes
- Give execution layer rewards to NOs; NOs pay the pool based on average execution layer rewards