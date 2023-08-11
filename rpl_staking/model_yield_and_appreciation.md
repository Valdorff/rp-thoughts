### RPL Value for potential sensitives
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
before_current152 = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 45544e-6 = 843.20 ETH/yr
after_current152 = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 45620e-6 = 844.73 ETH/yr
swap_yield_current152 = (after_current152 - before_current152) / 8 = 19.12%
before_prop = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 17411e-6 = 508.25 ETH/yr
after_prop = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 17488e-6 = 509.80 ETH/yr
swap_yield_prop = (after_prop - before_prop) / 8 = 19.27%
before_current148 = 300 * 16 * 1.14 * .055 + .7 * .05 * 19.55e6 * .0174 * 44937e-6 = 535.98 ETH/yr
after_current148 = 300 * 16 * 1.14 * .055 + 8 * 1.42 * .055 + .7 * .05 * 19.55e6 * .0174 * 44886-6 = 836.00 ETH/yr
swap_yield_current148 = (after_current148 - before_current148) / 8 = 0%
```
The ones who get the most yield from swapping see extremely similar results under both rulesets. On
the other hand we see a large difference in yield gained by swapping between just above and just
below the 150% cutoff under the current rules. This is because just below it, swapping activates no
extra RPL yield, where just above it, it activates 150% bonded ETH RPL yield. This is effect will
do two things: (a) it incentivizes people to _hold_ RPL if they drop below 150% - if they were on
the edge just above 150% then the big decrease in APR (no activated RPL on swap) should make it
unpalatable to sell RPL to make LEB8s; (b) it incentivizes people to _sell_ RPL if they rise above
150% - if they were on the edge just below 150% then the big increase in APR (activated RPL on swap)
should make it a no brainer to sell RPL to make LEB8s. This is an interesting quirk of the current
setup, where we essentially make a significant set of folks converge on 150% bonded ETH as their
strategy, even if they have relevantly different expectations

| ![image](./imgs/apr_and_appreciation.png) |          ![image](./imgs/apr_and_appreciation_zoom.png)           |
|:-----------------------------------------:|:-----------------------------------------------------------------:|

#### Reading these charts
- The x-axis is per-year ratio appreciation expectation as explained in [the model](#the-model)
- The red line is current "Net RPL" based on RPL rewards plus that expected appreciation
- The green line is the proposed plan for the node that loses the most yield (only EB16s with
  exactly 24 ETH worth of RPL each).
- The green dashed line is the best yield benefit to swapping from RPL to an LEB8 w/the proposed
  rules as explained in [the model](#the-model)
- The red dashed line is the best yield benefit to swapping from RPL to an LEB8 w/the current
  rules; not how close it is to the proposed rules
- The red dotted line is the yield benefit to swapping from RPL to an LEB8 w/the the current rules
  if you're _just_ under maximum
- black line is the best yield benefit to swapping from RPL to an LEB8 w/the proposed rules
- For the proposed rules: if we are on the green line below the dashed green line, it may make sense
  to swap RPL to make an LEB8; this happens if our expected ratio appreciation is < ~16% per year
- For the current rules: if we are solidly above 150%, we'd use the dashed red line and find that it
  may make sense to swap RPL to make an LEB8 if our expected ratio appreciation is < ~11% per year
- For the current rules: if we are solidly below 150%, we'd use the dotted red line and find that it
  may make sense to swap RPL to make an LEB8 if our expected ratio _depreciation_ is < ~7% per year 
 

#### Conclusions from this model
First looking at people above 150%: we can bound the people that "should" be nudged into a lower RPL
allocation to those that believe RPL will grow more than 11% per year, but less than 16% per year.
Additionally, if they hold significant RPL beyond 150% (earning no yield), we know they're not
sensitive to RPL APR.

On to the key group - the potential sensitives. We can now better define the maximum possible RPL
rationally sold as:
- Held by potential sensitives from the [NO pie chart](readme.md#which-nos-are-sensitive-to-rpl-yield)
  - Currently above 10% borrowed ETH, currently below 150% bonded ETH, not holding a lot of liquid RPL
- In the 5.5% potential sensitive slice from the [RPL weighted pie chart](readme.md#which-nos-are-sensitive-to-rpl-yield)
- Believe RPL ratio trajectory is from 0.93x to 1.16x per year
  - Fairly neutral with some "lean bullish"
  - For context if that pace kept up 3 years, RPL would be at 80%/156% the current ratio

These are maxima assuming everyone is at exactly the minimum RPL APR they'll accept, that everyone
is comfortable fully swapping to LEB8s, that all potential sensitives believe in the RPL trajectory
above (or even tighter for the ones that have any LEB8s or are further form 150%).

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