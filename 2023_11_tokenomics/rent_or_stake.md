


The premise of this idea is that there is a cost to holding RPL for a period of time, and we should be able to really quantify it and... charge people that amount.

Let's start by explaining the idea, and then trying to put numbers to it.

## The general idea
- There are 2 classes of nodes
  - RPL stakers
  - RPL renters
- RPL renters
  - Pay a fee, X, when depositing
  - Have a rent expiry time set to 2 years later
    - This creates significant alignment; assuming renters rent evenly over time, renters would average being one year away from expiry 
  - If rent expires, anyone can force-exit them
  - During last 6 months of rent, can pay rent again to extend expiry time by 2 years
  - Get vote power TBD, based on their rent
- RPL stakers
  - Stake at least Y% of borrowed ETH as RPL in order to deposit
  - Get RPL rewards if over Y% of borrowed ETH at the end of a period
    - Includes inflation share
    - Includes RPL rental fees

## Getting numbers
Let's play with it a bit...

If we assume Y=10, as it currently is, what would be a sensible X?
At maturity, assuming all RPL is staked, the cost of holding RPL is based on supply inflation, minus the rewards that go to staked RPL
- `.05*(1-.7)*(.1*borrowed_ETH) = .0015*borrowed_ETH/year`
Does that mean a good value for X is `.003*borrowed_ETH`?
If it was, the rational choice is to rent because it has lower (zero) volatility.

Nonetheless - let's assume we go with X=.003*borrowed_ETH and see where we land...
Context from `/tvl` RocketWatch command:
```
Staking Minipools: 825,837.13 ETH
├─rETH Share:      560,021.00 ETH
└─Node Share:      265,816.13 ETH
```
Ok, so we said the rational choice is to rent. Let's assume 10% of people do it and see where that puts us. The total cost of the 90% staking is `.05*(1-.7)*(.1*(.9*560k)) = 756 ETH/yr`. The 10% would pay rental fees of `.003*.1*560k/2yr = 84 ETH/yr`. This means that the cost to hold RPL is now actually `.0015*borrowed_ETH/year*(1-84/756)=.00133*borrowed_ETH/year` -- essentially, if the price of RPL vs ETH stays steady, it's now 11.1% cheaper to be a staker than a renter. 

TODO: redo but competing with CSM

At 50% renting, we get a total cost of staking of `.05*(1-.7)*(.1*(.5*560k)) = 420 ETH/yr`. The 10% would pay rental fees of `.003*.5*560k/2yr = 420 ETH/yr` -- here the cost of holding RPL is zero, while the renters are still paying not-zero. In this case, the only reason to rent is a bet against RPL over the next 2 years. Note that this isn't crazy at all -- the rent is only 3% the stake amount over 2 years.

## Valuation
Let's pretend the 10% renter case is where things settle out. How would we do a valuation model for RPL here?

We're currently using something like the following (pretending it's all LEB8):
```
implied_ratio = (rETH_TVL * RPL_value_per_pool) / (RPL_supply * protocol_ETH_per_pool)
implied_ratio = ((560,000 * 1.0907) * 2.4) / (19.9e6 * 24) = .00307
```
In this case, the "RPL_value_per_pool" term will be 2.4*.9, since only 90% of pools provide RPL. The rest should hold steady.
But! We somehow need to account for having revenue :thinking:.


### Lol... this math is dramatically wrong fails, but it's bedtime
If you have a desired APY for your capital in general, we could do: 
```
implied_ratio_component_staking = (rETH_TVL * RPL_value_per_pool) / (RPL_supply * protocol_ETH_per_pool)
implied_ratio_rent = RPL_supply*apy/ETH_revenue - implied_ratio_component_staking
implied_ratio = implied_ratio_component_staking + implied_ratio_component_rent
```

```
implied_ratio_component_staking = (rETH_TVL * RPL_value_per_pool) / (RPL_supply * protocol_ETH_per_pool) = ((560,000 * 1.0907) * (2.4*.9)) / (19.9e6 * 24) = .00276
implied_ratio_rent = RPL_supply*desired_RPL_apy/ETH_revenue - implied_ratio_component_staking = (19.9e6*.03/84) - .00276 = 7107 - .00276
... xD that aint right
implied_ratio = implied_ratio_component_staking + implied_ratio_component_rent
```

```
math scratchpad work
RPL_revenue/RPL_supply = apy
ETH_revenue*implied_ratio/RPL_supply = apy
ETH_revenue*(implied_ratio_rent+implied_ratio_component_staking)/RPL_supply = apy
(implied_ratio_rent+implied_ratio_component_staking) = RPL_supply*apy/ETH_revenue
implied_ratio_rent = RPL_supply*apy/ETH_revenue - implied_ratio_component_staking
```

### Variations/extensions
- Instead of nodes being stake/rent-based, could be minipools
  - Shouldn't change any relationships, just implementation (since people could have one of each node type, as an alternative)
- Can only kick RPL renters when we have "enough" supply
- Allow the rent to be paid in ETH and just exchange it for RPL before rewards? Or don't bother? Shouldn't really matter.
- What happens if the rent is too high for people to want to pay it?? I think that actually breaks the whole thing, which isn't great. This is inherited from the current system where the minimum bond is fixed -- here the rental fee derives from that, so it is similarly brittle.
  - We would need a heuristic to choose when to (raise or reduce) the (minimum_rpl_bond and rental fee).
  - !! Actually... maybe I'm overthinking this. For an LEB8, we're proposing a fee of `0.003*24=.072 ETH/2yrs`. Meanwhile the benefit is commission of `solo_apr*24*.14 ETH/yr`. We can simply say "break-even rent is when the benefit equals the cost", which means: `.072/2 = solo_apr*24*.14`; ` solo_apr = .072/(2*24*.14) = .0107`. So this rent should be attractive as long as solo_apr is above that (plus some amount to account for gas and protocol risk). We could probably have a heuristic for the pDAO to update the rent based on solo apr.

## Early sandbox version of the idea
RPL ticket -- burn a one-time amount to enter. Doesn't serve as collateral.
Vote could be done easily enough by borrowed ETH, eg, which still required an amount of RPL initially.
I think this is interesting b/c it lets us essentially set a time horizon that makes sense.
Danger -- account resale. Is the validator key (aka slashing) risk sufficient to prevent that from happening?

Could we model the equivalent price to "stake" or "burn" in terms of value capture?
If so, this would let users rent or buy according to (a) time horizong and (b) volatility exposure concerns