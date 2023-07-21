# [DRAFT] RPL Staking Analysis and Initial Suggestion
July 2023

## High level RPL-staking options

### [DRAFT] Visualized rule sets

![image](./imgs/rule_summary.png)

### [DRAFT] Current rules

- "Minimum" RPL stake is 10% of borrowed ETH (aka protocol ETH, pETH, matched ETH)
  - You must be over this threshold _including_ a new minipool to launch a new minipool
  - You must be over this threshold at rewards snapshot time to be eligible for RPL rewards
- Maximum effective RPL stake is 150% of bonded ETH (aka NO ETH, nETH, provided ETH)
  - Up to this much RPL at rewards snapshot time can be eligible for RPL rewards
- The NO share of inflation gets split up per-effective-RPL

### [DRAFT] "Knoshua" rules
- "Minimum" RPL stake is 10% of borrowed ETH (aka protocol ETH, pETH, matched ETH)
  - You must be over this threshold _including_ a new minipool to launch a new minipool
  - You must be over this threshold at rewards snapshot time to be eligible for RPL rewards
- Only the minimum is "effective".
- If you're below 10% of borrowed ETH, you get no rewards
- The NO share of inflation gets split up per-effective-RPL

### [DRAFT] Proposed rules
- "Minimum" RPL stake is 10% of borrowed ETH (aka protocol ETH, pETH, matched ETH)
  - You must be over this threshold _including_ a new minipool to launch a new minipool
  - You must be over this threshold at rewards snapshot time to be eligible for RPL rewards
- Rewards are based on weight
  - If you're below 10% borrowed ETH, weight is 0
  - From 10%-15% borrowed ETH, weight is linear with the amount of borrowed ETH
  - Above 15%, weight follows a logarithmic curve, rising forever, but ever-more-slowly
- The NO share of inflation gets split up as weight/total_summed_weight

## The proposed plan
- Take up the "Proposed rules" above in order to:
  - Reward primarily based on borrowed ETH, as this is what allows RP to meet rETH demand
  - Discourage large-scale speculation while getting RPL yield from the protocol
    - Encourages speculative holdings either exposed to inflation, or active in defi
  - Keep active rebalancing for good performance minimal. Importantly, there should be essentially
    no downside to being slightly above the minimum (including opportunity cost)
  - The rules will apply to all validators including new ones and currently running ones.
- Move the minimum to withdraw to 15% borrowed ETH (the end of the linear region)
  - This minimizes how "locked" users are, while also acknowledging that RPL is highly volatile; we
    don't want to encourage users to end up below the "minimum" used to start a minipool
- Change the time lock to add withdrawal friction
  - Make withdrawal a 2-step process. Set X RPL to "withdrawing"; these RPL are no longer eligible
    for rewards or voting. After a time period (make a settings; start it at 28 days), the RPL may
    be withdrawn.
  - There were worries that allowing withdrawal to lower thresholds would cause a lot of RPL to be
    withdrawn. While that can happen today, it has a lot of organic friction from exiting minipools
    and recreating them -- its worth noting that (A) RP doesn't control the exit/entrance queues,
    (B) RP doesn't control gas prices, and (C) while people are exiting/entering they are not
    earning rewards for themselves or rETH. The proposed lock time allows us to control the amount
    of friction entirely. This sort of system is very common in Cosmos staking.
  - Get rid of the cooldown on stake. Allow stake-on-behalf without limitations.
  - There has been talk about tracking stake at all times instead of just at the snapshot time; I
    believe this would be extremely challenging in a post-oDAO world, and we should be designing
    with that in mind
- Phase in the new rules slowly
  - For rewards, this can be achieved by calculating the "share of the pie" for both rule sets, and
    then adding them together in a changing proportion.
    - Period X after the vote: `0.17*x*proposed_share + 0.17*(6-x)*current_share`  
    - After period 5, simply used proposed_share
  - For the withdrawal threshold, it's a little complicated. First, it requires a pDAO guardian
    action, so we don't want to do a ton of changes. Second, the current setting is based off of
    bonded ETH, _not_ borrowed ETH. This means 16-ETH minipool holders will have a higher withdrawal
    threshold than intended. Still, it will be much lower than the current one (less than a third).
    - After Period X=3 rewards go out, set withdrawal threshold to 100% bonded ETH
    - After Period X=6 rewards go out, set withdrawal threshold to 45% bonded ETH
      - This is equivalent to the desired 15% borrowed ETH for LEB8s; unfortunately, it's 45%
        borrowed ETH for 16-ETH minipools, but that's the best we can do without a SC change
    - In the next planned Smart Contract release, update to be based on borrowed ETH
      - Once active, set withdrawal threshold to 15% borrowed ETH
- Don't impact voting -- keep that using 0.5*sqrt(min(rpl, 150%_bonded_eth_value_in_rpl))
  - Not taking a position on whether this should change, but if that's desired it can be an
    independent proposal

## A more detailed comparisons between rule sets

### [DRAFT] Current vs Knoshua
|   ![image](./imgs/rule_kc.png)   |   ![image](./imgs/operators_kc.png)   |
|:--------------------------------:|:-----------------------------------:|
| ![image](./imgs/rulediff_kc.png) | ![image](./imgs/operatorsdiff_kc.png) |

- When providing the same amount of rETH supply (aka, at one point on the x axis), the current rules
  have a massive variation in RPL rewards of up to 15x based on the amount of RPL staked. Knoshua's
  rules have zero variation.
- Knoshua's plan _strongly_ favors people that are RPL-hesitant and want to join with low exposure.
  For folks at the minimum, they'd see their rewards ~4.3x
  - This also makes it easier to attract new NOs since the higher rewards can defray the up-front
    RPL price risk
- Knoshua's plan would see the median current NO get ~2x the rewards of the current plan
  - A fair number of NOs end up lower than current rewards.
- Knoshua's plan strongly favors LEB8s. This aligns RPL rewards to what helps the protocol (the
  ability to meet rETH demand).

### [TODO] Current vs Proposed
|   ![image](./imgs/rule_pc.png)   |   ![image](./imgs/operators_pc.png)   |
|:--------------------------------:|:-----------------------------------:|
| ![image](./imgs/rulediff_pc.png) | ![image](./imgs/operatorsdiff_pc.png) |

- When providing the same amount of rETH supply (aka, at one point on the x axis), the current rules
  have a massive variation in RPL rewards of up to 15x based on the amount of RPL staked. For the
  proposed rules, that variation is down to ~3x (technically, the log gains continue indefinitely
  but with aggressively lowering marginal benefit; here I used 12 ETH worth of RPL staked on an LEB8
  as a realistic "limit")
- The proposed plan _strongly_ favors people that are RPL-hesitant and want to join with low
  exposure. For folks at the minimum, they'd see their rewards ~2.44x
  - This also makes it easier to attract new NOs since the higher rewards can defray the up-front
    RPL price risk
- The proposed plan would see the median current NO get over 2x the rewards of the current plan
  - Very few NOs would see a decrease in their rewards (only 16-ETH minipool holders with more than
    8.1 ETH of RPL staked per 16-ETH minipool)
- The proposed plan strongly favors LEB8s. This aligns RPL rewards to what helps the protocol (the
  ability to meet rETH demand).

### Try it out!
There's a calculator you can use to see the share received by a node at
https://www.desmos.com/calculator/o71k2vz1qt

It takes in the number of LEB8s, the number of EB16s, and the amount of RPL staked (in ETH).
It returns out how many millionths of the total reward you'd get under each system, assuming the
current allocations; the higher this number is, the more the node will earn. Note, no graph is
expected -- the results are the ppm numbers on lines 10, 12, and 14.

## Brass Tacks

### Expanded Rationale
This is touched on some in [the proposed plan](#the-proposed-plan) section, but it's worth giving a
bit more space. Funds should be used to achieve protocol goals - ie, they should be used to convince
people to do the things that benefit RP.

- We are spending money badly 
  - Having a lot of bonded RPL on a node is no better for the protocol than a bond near the minimum
  - We currently spend 55.2% of rewards on stake beyond 30% pETH (see `heavy_spend()` in
    `rewards_plot.py`). We had a lot of complaints about oDAO spend (15% of inflation). This is 35%
    of inflation.
  - RPL-as-collateral: any collateral use case _must_ work with the minimum
    - For MEV, attackers aren't likely to put up more than is required
    - For correlated slashing, RPL liquidity won't allow effective liquidation of even the minimum,
      let alone additional RPL beyond the minimum.
  - "Protected speculation" is a term I once used for the "benefit" of RPL rewards at high node
    collateral. Our system of inflation is opinionated and does _not_ reward speculation outside the
    protocol; I don't see a benefit to reward it within the protocol either, as it doesn't achieve
    protocol goals.
  - Note: Some amount of RPL beyond the minimum is a convenience -- a buffer so the NO doesn't need
    to be highly active. We should keep that if possible, as the proposed plan aims to.
    
- We need the ability to meet rETH demand
  - We should scale rewards on pETH, which is directly related to meeting rETH demand.
    - This implies we'll favor LEB8s over EB16s because they more efficiently meet rETH demand.


### RPL Value (a model combining appreciation and rewards)
Some people have mentioned fears of this proposal causing a sell-off from RPL-heavy folks.
I don't see this at all. This proposal better aligns incentives and is a win for everyone.

#### The model
We can model expected price appreciation against ETH as an APR. For example, if you expect price to
double within 2 years, you can get an apr of `2^(1/2) - 1 = 1.41 - 1 = 41%`. If you use your risk
adjusted expectation (eg, you'll call it 1.8x to make up for high risk, even though you think it has
a 2x EV), you can include that too (in this case that would be 34%).

The other thing we need to model is what the best results we can get from selling RPL are.\
To model this, we'll start with a very RPL-heavy (152% bonded ETH) node that has 300 EB16s. Then
we'll compare the yield for one year vs the yield for one year if they sell 8 ETH worth of RPL in
order to make an LEB8. We will value RPL rewards at the current ETH ratio -- this isn't right based
on our x-axis, but we'll ignore for simplicity here (the effect is small vs on the RPL principal).

```
before_current = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 45544e-6 = 843.20 ETH/yr
after_current = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 45620e-6 = 844.73 ETH/yr
swap_yield_current = (after_current - before_current) / 8 = 19.12%
before_prop = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 17411e-6 = 508.25 ETH/yr
after_prop = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 17488e-6 = 509.80 ETH/yr
swap_yield_prop = (after_prop - before_prop) / 8 = 19.27%
```
Note that there's very little difference in yield gain from switching 8 ETH worth of RPL to a new
LEB8 between the two rulesets.

| ![image](./imgs/apr_and_appreciation.png) |          ![image](./imgs/apr_and_appreciation_zoom.png)           |
|:-----------------------------------------:|:-----------------------------------------------------------------:|

#### Reading these charts
- The x-axis is per-year ratio appreciation expectation as explained in [the model](#the-model)
- The blue line is current "Net RPL" based on RPL rewards plus that expected appreciation
- The orange line is the node that loses the most by swapping to the proposed plan (only EB16s with
  exactly 24 ETH worth of RPL each).
- The gray line is the best yield benefit to swapping from RPL to an LEB8 w/the current rules as
  explained in [the model](#the-model)
- The black line is the best yield benefit to swapping from RPL to an LEB8 w/the proposed rules
- For the current rules: if we are on the blue line below the black line, it may make sense to swap
  RPL to make an LEB8. This happens if our expected ratio appreciation is < ~11% per year 
- For the proposed rules: if we are on the orange line below the gray line, it may make sense to
  swap RPL to make an LEB8. This happens if our expected ratio appreciation is < ~16% per year 

#### Conclusions from this model
Based on the above, we can bound the people that "should" be nudged into a lower RPL allocation to
those that believe RPL will grow more than 11% per year, but less than 16% per year. **This is a
_narrow_ band, so we wouldn't expect a lot of people to be in that band.**

#### How lower rewards can be a win (specific example)
We'll run the model backwards here. Let's assume a person with EB16s at 100% collateral that
believes RPL will 2x in 2 years.

- Their APR loss in going from the current to the proposed rules is ~2.6% APR
- This can be multiplied by their "per-year ratio appreciation expectation" of 1.41 to get their
  break-even RPL appreciation improvement
- `1.41*.026 = 3.7%`

This is a modest, but real improvement. Does it seem realistic that the proposal would have such an
impact? To me it does, but this is very far into subjective. Some factors that could help:
- Higher rewards attract more minipool creation, which helps us meet rETH demand
- Higher rewards create a minipool queue, which boosts rETH APR and helps _create_ rETH demand
- Better-aligned incentives improve trust in the protocol
  - Makes the protocol more investable
  - Since NOs must hodl RPL, that can also attract NOs

#### The model is a model
This is _just_ a model - the map is not the territory. It's likely some folks are spooked by change,
and perhaps by "number go down" on the rewards front. On the flip side, it's also possible that
some folks are galvanized by improvements and setting RP up for growth.

I don't see any reason to expect a large-scale sell-off. I believe this proposal makes RP better and
helps us attract more NOs. I believe better RP is (eventually, on average) reflected in RPL.

### [DRAFT] Why change? People entered with this ruleset.

I believe consistency is important. We shouldn't change things just because we can. That said, I
also don't believe we should totally shackle ourselves forever based on past decisions.

Let's start with another question -- where does the current ruleset come from?
- The minimum
  - Initial design by fireeyes -- no insight into reasoning
  - Often used in RPL price models to set the fundamental floor value of RPL 
  - When we added LEB8s, we wanted to keep the fundamental floor value in those models unchanged,
    which is why we went with keeping it constant as a percent of borrowed ETH
- The maximum
  - Initial design by fireeyes -- no insight into reasoning [?? IS THIS RIGHT?]
  - There was a rather stressful vote when adding LEB8s about whether the maximum should be 150% of
    borrowed ETH, 150% of bonded ETH, or flat per minipool
  - During that vote, there were attempts to justify the original 150% number for 16-ETH (so that 
    we could better understand what it meant to minimize change). The best reason I saw was that it
    served as "protected speculation" for heavily RPL-aligned individuals.
  - There was an interaction with the minimum threshold to withdraw until Redstone. It was possible
    to instantly stake RPL and have that affect rewards, so if people could withdraw at will, they
    could get all the benefits of max stake while only having the RPL staked for a moment. [?? IS 
    THIS RIGHT? DID WE HAVE THE TIMELOCK BEFORE REDSTONE?]
- Keeping the rules the same
  - All else being equal, stability is good
  - Right now we're rewarding speculating within the protocol, rather than creating rETH supply
    - This is _not_ aligned with the protocol's needs, which is a suitably important reason to make
      changes.
  - Now that we're post-Shapella, people can exit if the rules truly don't suit them. This makes it
    less critical to keep things exactly the same