## Table of Contents
1. [Choose your depth](#choose-your-depth)
2. [Suggested support](#suggested-support)
2. [Staked RPL... or all RPL](#staked-rpl-or-all-rpl)
3. [Other considerations](#other-considerations)

## Choose your depth
🛑🛑 Please stop for a moment 🛑🛑

This document is the third tier of importance.

If you feel comfortable with everything in the top tier, by all means feel free to continue. But if you don't, please focus on that and ask questions. 

The sections below are tiny details compared to the stuff in higher tiers. Most readers should feel free to ignore this document.

- [Top tier](readme.md)
- [Tier 2](readme_tier2.md)
- [Tier 3](readme_tier3.md)

## Suggested support
- Remove opt-in upgrades
  - They add very little security as we have withdrawals now; meanwhile, they make code maintenance and testing much harder as more states are possible.
- Voting power
  -  The [pDAO charter](https://rpips.rocketpool.net/RPIPs/RPIP-23) defines the pDAO as "Node Operators, with power based on effectively staked RPL"
  - I read this plainly as requiring (a) Node Operation, (b) staked RPL, (c) a definable "effective" criteria.
  - Thus far, effective has meant "up to the value of 150% of bonded ETH"
  - I propose simply leaving that unchanged, but keeping an eye on this (eg, track voting power over time). If we see most users splitting off into ETH-only or RPL-only, power could grow concentrated here.
  - Brainstorm A: Add a small financial benefit to governance, eg:
    - 1-2 times a year send RPL from treasury out based on:
      - Vote power used directly during that period (100% weight)
      - Vote power used via delegate during that period (99% weight)
      - Vote power used on behalf of others during that period (1% weight)
        - Yes, I'm a large delegate - if it becomes a distraction that a large delegate is suggesting this, I can commit my share as charity to the EFF
  - Brainstorm B: Require ETH and RPL to work together 
    - Use the current rules for vote power. Allow any node to point their bonded ETH weight at an RPL-holding delegate node and their RPL weight at an ETH-holding delegate node
    - Vote power of a node is, eg, `sqrt(min(node_RPL, 1.5*delegated_bonded_ETH_weight)) + sqrt(max(delegated_RPL_weight, 1.5*node_bonded_ETH_weight))`
    - Note that folks can opt to delegate to their own node if they hold both.
    - Note that this idea would likely need a change to the pDAO charter (which "requires a 2/3 or greater supermajority pDAO vote").
- MEV penalties
  - Allow-listed relays
  - No vanilla blocks allowed
  - oDAO-applied penalty based on size of theft (largest bid across relays) plus a little bit (eg, 10%)
    - Note: no penalty for missing, just for using vanilla block or a non-allowed relay
  - Some trickiness around relay API timeliness - don't expect them to be quite realtime
    - If APIs are bad, we may need to remove them from allowlist
  - Security council should be able to remove penalties -- note they can be replaced by oDAO, so this is insufficient
  - pDAO guardian must remain in place to limit total penalties
- rETH protection
  - Outlier underperformers (see ArtDemocrat's proposals) should pay restitution to rETH to meet an adequate number (eg, overall rETH performance).
  - First restitution should be funded from ETH rewards flows
    - Per reward period: EL smoothie, RPL commission share -- both of these can be taken care of when making the merkl tree, so the underperformer never gains dominion over those funds
    - At this point, record any remaining unpaid restitution as debt
    - Debt can be repaid by:
      - EL fee distributor distribution -- anyone can do this
      - CL distribution -- anyone can do this
      - CL distribution during exit -- only owner can do this without a long wait.
        - Note that this exit can be a forced exit
        - Advanced forced exits: if performing badly routinely -- kick. This is better for rETH _and_ the NO.
- Set RPL inflation to 1.5% and end RPL rewards
  - In this structure, we don't need to use RPL inflation to get more people staking RPL to meet rETH demand. Insofar as folks have unstaked, they're at least doing a service to RPL stakers by giving up their share. If they're doing something like LPing, then they're further serving RP.
  - 1.5% means the oDAO and pDAO continue to receive the same amount - this just removes the portion that went back to NOs.


## Staked RPL... or all RPL?
Right now the rewards in this proposal go to staked RPL. There are some efficiencies to be gained by rewarding _all_ RPL instead, as well as some challenges.

Benefits:
- Since the capital doesn't need to be staked, that allows it to be _used_
  - The two main uses that come to mind are LPing and using it as collateral for a loan
- If value can be accrued to the token, this translates to capital gains tax instead of income tax (may be jurisdiction and execution dependent).

Challenges:
- Governance is the big one imo
  - We would need to redefine the pDAO (which means a 2/3 vote to change the charter)
  - We would need to figure out voters
    - Right now, the "RPL-staking node operator" is a really nice overall proxy; while rETH isn't directly represented there, making rETH attractive has a direct benefit to RPL via market size
  - I'm really struggling to think of something. The best I've come up with is having specific contracts where RPL stake is counted for vote power (eg, Uniswap pools, Aave collateral, etc). The downside is that we'd need to explicitly add contracts, wouldn't be able to add anything upgradable, would likely need to code little adapters to get RPL stake, etc. Obviously, small/new contracts would probably not be supported. We might need caps of some sort, so that a contract failure cannot jeopardize RP governance.
- Community would be the related thing: I think it would make it easier to have RPL holders/users that are less-involved with the RP community

Execution:
- Brainstorm A: ETH goes to a treasury. Every so often the treasury buys RPL with that ETH (eg via an auction)
- Brainstorm B: RPL can be burned against the treasury based on a fairly long TWAP (eg on uniswap pool). This would mean that if there's ever a dip, it's profitable to buy and burn RPL. Essentially, this is a market buy that happens on an ongoing basis.

## Other considerations
- This looks super attractive for ETH-only NOs - what if folks get stuck in a giant queue?
  - Brainstorm A: Can we track the spot in the queue without requiring the beacon contract deposit ahead of time? If so: (a) more of the bond can be passed on to the deposit pool, and (b) it becomes possible to request a minipool queue exit. For the latter, it would just reserve some ETH in the deposit pool for requested exits (or, mint rETH and let you exit that way).
- It's not clear to me how migrating to megapools should work.
  - Can we have a mix of minipools in a megapool and legacy minipools? I think that should be ok from a technical standpoint...
  - Having worse capital efficiency, zero RPL rewards from inflation, and being gassier should make them pretty unattractive pretty fast imo. 
  - Maybe this is simply "don't shatter if people have both" and the rest will handle itself.
- What if we change our mind about bond curve?
  - I think the curves can essentially be represented by three numbers: number of anchor minipools, anchor minipool size, additional minipool size.
  - If we change our mind, I think that'd be ok. We'd essentially want a way to designate new anchor minipools, or resize the existing ones -- the credit system might make that not-too painful?
- Explicit non-change: there should be unbonding time for staked RPL. We already have that from RPIP-30, and I just want to explicitly note it will continue to apply and apply regardless of whether someone is RPL-only or also an NO with bonded ETH.