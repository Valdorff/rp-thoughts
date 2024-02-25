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
A core tenet of this idea is simplicity. It does not have many dynamics as a result. But there's a couple things to keep an eye on: 
- The commission to NOs is set purposely high at 5%. If we grow comfortably and NO supply is never ever an issue, we should lower it (and increase RPL share). This is primarily based on competitive landscape. Based on current outlook, I believe it could go as low as 3% if we meet all our growth goals. My advice to RPLers: don't be short-sighted -- reward NOs enough that they are not blockers to our growth (this is why I'm suggesting starting it at a place that's likely "too generous").
- What do we do if rETH demand slackens before meeting our growth targets?
  - Voters determine whether to spend on demand or not, with the expense coming from RPL. RPL will, ofc, benefit from growth -- so it's very likely that this "spend" is worthwhile.
  - The first way to spend is trivial: reduce the portion to RPL stakers, and rETH's share grows commensurately.
  - The second way to spend allows more fine-grained control. Here we instead increase RPL inflation and spend the RPL in ways that cause rETH demand. For example, we could increase liquidity incentives to rETH/WETH, or incentivize the use of rETH in lending markets.
  - Essentially the question is along the lines of "do I get more TVL on board by increasing the benefit a little to _all_ users, or more significantly to _some_ users"? The answer is difficult to get at and will vary with context.
- There is a conflict of interest with "Voters" being able to change "Voters" slice. I propose our vote also commits to a simple heuristic like:
  - If <40% of RPL is contributing vote power in RP, we SHOULD increase this slice
  - If <30% of RPL is contributing vote power in RP, we SHALL increase this slice
  - if >80% of RPL is contributing vote power in RP, we SHOULD decrease this slice
  - if >90% of RPL is contributing vote power in RP, we SHALL decrease this slice
  - if 30-80% of RPL is contributing vote power in RP, we SHALL NOT change this slice
  - require a 2/3 or even 3/4 supermajority vote to change this

## RPL buy+burn thoughts
  - A share of ETH from commission goes to a smart contract 
  - Users may call a function to swap RPL for the ETH in the above contract
  - Swap price is based on on-chain TWAP oracle
  - Any RPL swapped this way is burned by sending it to `0x000000000000000000000000000000000000dEaD`

There may be challenges around very discrete distributions, especially predictable ones like the smoothing pool distributions. A related challenge might come from large NOs that can distribute and trade in a single bundle - this could give them a protected arbitrage opportunity. One way to mitigate this genre of issue is to stream in the available funds.

Here's an over-simple implementation:
- `available_eth = (unlock_rate * (current_block - last_deposit_block)) + previously_avaiable_eth`
- When funds are deposited
  - `previously_avaiable_eth = available_eth`
  - Update `last_deposit_block`
  - Set `unlock_rate` to `(balance - available_eth) / 201600` (this means if there were no additional deposits, everything would be unlocked within 28 days)
This isn't great as deposits essentially extend the time to fully unlock funds from any one deposti back up to 28 days. This could use work, but seems tractable.

## Voter share thoughts
I am currently suggesting rewards to be split based on number of RPL contributing to vote power. Since we provide vote power up to 150% of bonded ETH, a node would earn based on `min(1.5*bonded_eth, rpl_value_in_eth)`; their share would be that number divided by the sum of all nodes using that same equation. This is a rather new idea, and there's other variants worth looking at:

- Scale by vote power. This is very intuitive, but rewards sock puppets to avoid the quadratic scaling. In order to go this route, would need to show that the benefits of staying on one node due to bond curves outweigh the benefit of using sock puppets to scale this reward. Imo, it's fine if there's a crossover, as long as the crossover is high (eg, >1k bonded ETH).
- Use a lower maximum for rewards, eg, `min(1.15*bonded_eth, rpl_value_in_eth)`. If the quadratic method can't be done with confidence, a lower maximum may be used to encourage small stakers to have vote power.
- Base on _active governance_ (actually voting/delegating to someone that actually voted) rather just the potential to vote.

## Modeling
[TODO] is this unchanged? need to think more.

I like to have _some_ model of value available.

I made a [spreadsheet](https://docs.google.com/spreadsheets/d/18cc6smtFn1dETLRuF1RPa4sF8Fx8uOPg41eJn3AaGAA/edit#gid=0) using one methodology and taking quick looks at a handful of scenarios.

This is in the spreadsheet too, but I want to re-emphasize: this fundamental value ratio != price by a long shot. See cell A24 for a whole lot of caveats 😛. Shoutout to @luominx, who made an earlier variant of this model for themselves and shared it with me.  

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