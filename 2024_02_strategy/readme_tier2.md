## Table of Contents
1. [Choose your depth](#choose-your-depth)
2. [Dynamics](#dynamics)
3. [Stepping stones](#stepping-stones)

## Choose your depth
🛑🛑 Please stop for a moment 🛑🛑

This document is the second tier of importance.

If you feel comfortable with everything in the top tier, by all means feel free to continue. But if you don't, please focus on that and ask questions. 

- [Top tier](./readme.md)
- [Tier 2](./readme_tier2.md)
- [Tier 3](./readme_tier3.md)

## Dynamics
My favorite thing about this idea is the simplicity. It does not have many dynamics as a result. But there's a couple things to keep an eye on: 
- The commission to NOs is set purposely high at 5%. If we grow comfortably and NO supply is never ever an issue, we should lower it (and increase RPL share). This is primarily based on competitive landscape. Based on current outlook, I believe it could go as low as 3% if we meet all our growth goals. My advice to RPLers: don't be short-sighted -- reward NOs enough that they are not blockers to our growth (this is why I'm suggesting starting it at a place that's likely "too generous").
- What do we do if rETH demand slackens before meeting our growth targets?
  - Voters determine whether to spend on demand or not, with the expense coming from RPL. RPL will, ofc, benefit from growth -- so it's very likely that this "spend" is worthwhile.
  - The first way to spend is trivial: reduce the portion to RPL stakers, and rETH's share grows commensurately.
  - The second way to spend allows more fine-grained control. Here we instead increase RPL inflation and spend the RPL in ways that cause rETH demand. For example, we could increase liquidity incentives to rETH/WETH, or incentivize the use of rETH in lending markets.
  - Essentially the question is along the lines of "do I get more TVL on board by increasing the benefit a little to _all_ users, or more significantly to _some_ users"? The answer is difficult to get at and will vary with context.

## Stepping stones
We are _currently_ struggling with NO supply. I suggest one of:
- LEB5s with current rules (and DAO-upgradable delegate)
  - Requires an SC release to piggyback on
    - It is not worth an audit cycle or delaying tokenomics rework for this alone
  - Given that forced exits are likely to be possible soon, plan to force exit any remaining LEB5s 2 years after the launch of LEB5s.
  - In my [leb_safety](../leb_safety/readme.md) work, I argue that, without forced exits, we have to defend from MEV theft _plus_ 0.64 ETH per year.
  - For 2 years we need 1.28 ETH plus whatever we're comfortable with assuming we have forced exits. I suggest that's around 4+1.28=5.28 ~= 5 (rounding down is based off of how many "bad case" assumptions are made, but LEB6 works fine too if people prefer)
- RPL loans
  - Fund a multisig with ~10k RPL for the first iteration of this program, which is enough for around ~500 LEB8s
  - Take collateral in the form of rETH/ETH BPTs (balancer liquidity tokens)
  - 2.5 ETH worth of RPL for 1 year; 80% LTV; up-front fee of 10% which is refundable if used "properly"
  - This means a user would:
    - post 3.26 ETH worth of rETH/ETH BPT using their node or withdrawal address
      - 3.01 are locked as collateral 
      - 0.25 are given to the multisig
    - After a year, if the node in question
      - (a) staked the RPL within a week of the loan
      - (b) started an 8-ETH minipool within two weaks of the loan, and
      - (c) kept bonded ETH at the level of (b) or higher for the year the 0.25 ETH fee is sent back to them
  - The assumption is that by the end of the loan term, ETH-only would be an option, so the user could freely repay their RPL and continue participating if that's their preference. If we'd like to do 1.5 years for increased user confidence, that would be fine too.