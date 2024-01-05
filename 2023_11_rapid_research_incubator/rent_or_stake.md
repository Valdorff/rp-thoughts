This idea is meant to address "Rapid Research Incubator" topic #2 and #1
  - #2 alternative value capture for RPL:
    - The bond remains a form of value capture
    - Rent received is a new form of value capture
  - #1 by breaking the hard requirement that NOs be RPL stakers, the market is able to balance RPL staking attractiveness and NO attractiveness. When holding RPL isn't seen as attractive, people will prefer to rent. This in turn will make RPL more attractive. Similarly, if holding is seen as more attractive than rating, most people will stake -- in the extreme we get the current state. Note also that this helps make it much easier for RP to grow TVL, which in turn has a value impact on RPL (staked and liquid).

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
  - Get vote power TBD, based on their rent? Should be much lower.
  - Can only pay rent if there's a need for supply. Eg: deposit pool is full for new rent, or deposit pool is at least 1/4 full for rent extension
- RPL stakers
  - Stake at least Y% of borrowed ETH as RPL in order to deposit
  - Get RPL rewards if over Y% of borrowed ETH at the end of a period
    - Includes inflation share
    - Includes RPL rental fees

## Getting numbers
Let's play with it a bit...

If we assume Y=10, as it currently is, what would be a sensible X?
At maturity, assuming all RPL is staked, the cost of holding RPL is based on supply inflation, minus the rewards that go to staked RPL: `.05*(1-.7)*(.1*borrowed_ETH) = .0015*borrowed_ETH/year`.
That means a good floor value for X is `.0030*borrowed_ETH` for a 2-year rental.
This equates to 0.072 ETH worth of RPL to pay "rent" for an LEB8 for 2 years.

A ceiling value is probably gated by the expected commission gained -- obviously if you pay more than commission, then that's not very attractive. Here we have `solo_apr*commission*borrowed_eth*2years`. With our current 14% commmision and 3% solo apr (current is 4.2%, but dropping) that would be `0.03*.14*borrowed_eth*2 = .0084*borrowed_eth = 0.202 ETH` for an LEB8 for 2 years.

For the remainder of this work, I'll use the geometric mean of that floor and ceiling as my "rental": 
`sqrt(.0084*.0030)=>.005*borrowed_ETH/2years` for an LEB8 or `sqrt(.072*.202)=.121 ETH/2years` for an LEB8.

Context from `/tvl` RocketWatch command:
```
Staking Minipools: 825,837.13 ETH
├─rETH Share:      560,021.00 ETH
└─Node Share:      265,816.13 ETH
```
Let's assume 10% of people rent and see where that puts us. The total cost of the 90% staking is `.05*(1-.7)*(.1*(.9*560k)) = 756 ETH/yr`. The 10% would pay rental fees of `.005*.1*560k/2yr = 140 ETH/yr`. This means that the cost to hold RPL is now actually `.0015*borrowed_ETH/year*(1-140/756)=.00122*borrowed_ETH/year` -- essentially, if the price of RPL vs ETH stays steady, it's now 18.7% cheaper to be a staker than a renter. 

At 50% renting, we get a total cost of staking of `.05*(1-.7)*(.1*(.5*560k)) = 420 ETH/yr`. The 50% would pay rental fees of `.005*.5*560k/2yr = 700 ETH/yr` -- here the cost of holding RPL is negative, while the renters are paying a positive amount. It may still be justifiable to prefer rent -- the rent is only 0.5% the stake amount over 2 years and certainty is a valuable commodity.

## Valuation
This has changed from a previous state (available in git history) that included a staking and renting value component.

### Value from stakers
Here I'll use the same model as in the current system:
`ratio = (rETH_TVL * RPL_value_per_pool) / (RPL_supply * protocol_ETH_per_pool)`

The premise is that if all the RPL is staked for the number of minipools we have, and the number stays roughly steady (some churn, but no trend), then that means the value of the RPL is enough to hit the minimum in this case (cuz ppl will top off to get rewards) but not much more (cuz at maturity holding RPL is a cost and why would you).

The main impact of the rent-or-stake structure here is that `RPL_value_per_pool` will be heavily impacted. For example if you have 10% of people rent, then `RPL_value_per_pool` will only be 90% of what it would be if everyone staked.

Let's do it out for today under 3 situations, assuming exact minimum RPL per pool and 100% RPL staked (worst case):
- 0% renters: `(560k * 2.4)/(19.9M * 24) = .00281 ETH per RPL`
- 10% renters: `(560k * (2.4*.9))/(19.9M * 24) = .00253 ETH per RPL`
- 50% renters: `(560k * (2.4*.5))/(19.9M * 24) = .00141 ETH per RPL`
- 90% renters: `(560k * (2.4*.1))/(19.9M * 24) = .00028 ETH per RPL`

### Value from renters
Renters do not factor into RPL value directly. Instead, they (a) support TVL growth and (b) generate revenue for RPL stakers, which makes staking more attractive.

### Total value
So. Why do we want any renters at all?

The first purpose is growth. Right now we're (very) supply limited. Imagine that turning renting on gets us to 50% renters because we double our TVL, now we're comparing:

No rent: `(560k * 2.4)/(19.9M * 24) = .00281 ETH per RPL`\
Vs double size and 50% rent: `((2*560k) * (2.4*.5))/(19.9M * 24) = .00281 ETH per RPL`

This means that we've been able to support a much larger set without any damage to RPL value. It _also_ means that RPL stakers will be getting rent. We've done similar math above, so we know this is about 1400 ETH/yr (that maps to an oversimplified 0.06 extra ETH per LEB8 per year). This isn't neither earth-shattering nor negligible; back of the envelope math got me a 6.5% increase to ETH revenue for LEB8s in this scenario. 

If this is the right way to think about value, we realize a few things:
- stakers benefit RPL value a lot more
  - renters incentivize more stakers 
- there is little benefit to allowing new renters unless we need more supply (eg, deposit pool is full)
- if we reach/approach our self-limit, we don't need to allow renting

### Variations/extensions
- Instead of nodes being stake/rent-based, could be minipools
  - Shouldn't change any relationships, just implementation (since people could have one of each node type, as an alternative)
- Don't kick RPL renters when we have "insufficient" supply
  - This makes renting slightly more attractive as there's a chance of free time. That also means staking is slightly less attractive. The main benefit here is to protocol stability when supply is needed. 
- Allow the rent to be paid in ETH and just exchange it for RPL before rewards? Or don't bother exchanging? Shouldn't really matter.
- What happens if the rent is too high for people to want to pay it?? I think this could hinder growth. The solution would be to reduce rent if needed to hit growth goals. There is definitely a balance here -- as we saw, there's a benefit to RPL of having a lower percentage renters and a benefit to RPL of having more TVL. 
- Note that we _do_ have a principal agent problem. The only collateral is illiquid. This could be ok (with forced exits, eg) or we could have something like rETH collateral if we felt it was really necessary.

## Acknowledgements
Thanks to NeverAnIsland for proposing the rental valuation model and bouncing some ideas with me.

Thanks to Samus for a number of minor fixes. 