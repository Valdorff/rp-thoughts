This idea is meant to address "Rapid Research Incubator" topic #2 and #1
  - #2 alternative value capture for RPL:
    - The bond remains a form of value capture
    - Rent received is a new form of value capture
  - #1 by breaking the hard requirement that NOs be RPL stakers, the market is able to balance RPL staking attractiveness and NO attractiveness. When holding RPL isn't seen as attractive, people will prefer to rent. This in turn will make RPL more attractive. Similarly, if holding is seen as more attractive than rating, most people will stake -- in the extreme we get the current state. Note also that this helps make it much easier for RP to grow TVL, which in turn has a value impact on RPL (staked and liquid).

## The general idea 
- Split up ETH commission to a component that goes to NOs and a component that goes to RPL stakers
- Make a new curve, somewhat similar to RPIP-30's that will be used for _both_ ETH commission and RPL rewards
  - ![direct2_curve.png](direct2_curve.png)
- Remove the requirement of staking RPL in order to make minipools

## Thoughts
- It may be worth reading the predecessor idea at [direct_capture.md](direct_capture.md). In both cases, we implement an entirely new method of value capture: "Rather than requiring it for minipools as a 'ticket to commission' by allowing minipool creation, it is a direct ticket to commission revenue."
- Based on the [Getting Numbers](direct_capture.md#getting-numbers) section of the predecessor idea, we set 22% of commission revenue to NOs and the remaining 78% to staked RPL.
  - This should keep valuation roughly the same
- I have suggested two main modifications from the RPIP-30 curve:
  - Start the linear ramp at 0% -- given the new value capture method, there is no longer a justification or reason to start at 10% or any other value. I think this is important.
  - End the linear region around 12%. My thought here is that, at maturity, we'd like folks to have incentives for a similar stake as in the current system. I am definitely not married to this -- it was the first thought about when it should get diminishing returns.
- By using a single curve for both ETH commission and RPL rewards, we are maximizing how opinionated we are about incentivizing the behavior embodied by the curve.

Pros:
- ETH-only minipools supported :)
- Simpler to explain value capture vs the indirect “minimum bond” requirement
  - ![Pie charts showing ETH and RPL revenue](direct_pie_charts.png)
- Pretty simple to explain ETH and RPL apys
  - ETH is just a single APY number
  - RPL is one ETH APY number and one RPL APY number
    - To achieve "single number", this is just the linear part based on last period. Can have a slider to see what going further would've gotten you last period.
- This system allows staking massive amounts of RPL to get more commission -- just like in RPIP-30, this is unattractive at the extreme due to the diminishing returns in the curve
- 1-2 fewer parties than the other ideas that enable ETH-only minipools
- Works well with current voting; see [voting thoughts](direct_capture.md#voting-thoughts)

Cons:
- We’d essentially be getting rid of RPL-as-collateral, since it’s not required. Right now, we don’t use it anyways (except in oddball megaslashing cases, where its utility is liquidity-limited). That said, it takes away our ability to have an “instant-speed” bond.
  - Might be able to mitigate with something like a rETH bond if seen as necessary
- 3.08% commission for NOs doesn't sound as sexy as 14% commission; this is mostly a communication problem, as it's the equivalent to the current situation with a minimum.

## Acknowledgements
Thanks to samus and sckuzzle for helping me see that [direct_capture.md](direct_capture.md) really wasn't getting me to a place I liked and a good road to get somewhere happy.