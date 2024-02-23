I'll be working here to clarify my understanding of strategy.
My initial intuitive take is in [overall_preference.py](../../2023_11_rapid_research_incubator/overall_preference.md)

So my initial post had 5 bullets:
- Bond curves
- Change RPL capture from minimum bond to cut of commission
- Protect rETH from outlier bad NOs
- Exit validator on ejection balance ~31 ETH
- Universal variable commission

Some quick thoughts and open questions:
- [key] Bond curves
  - Assuming we had zero new node operator ETH, what rETH supply could we support?
  - Run for each bond curve
  - Run "hot MEV market" numbers for the anchor validator and compare profitability with 10+ minipools. Confirm that there is no incentive to sock puppet for MEV theft, even in a hot MEV market.
- [key] Change RPL capture from minimum bond to cut of commission
  - I think this is pretty nearly _required_ to really make bond curves function. We won't find enough RPL omegabulls to run pools with 1.5 ETH and 3.05 ETH worth of RPL.
  - This combines with the bond curve above to determine where we look good vs competitors
  - How much new nETH does this really bring to the table?? Is nodeset likely to give us a relevant
    data point for what that looks like?
  - If we have a market-share based split, I think we might be able to _really_ juice the NO side to
    start and back it off as we capture market. This might present a way to have our cake (market
    share by big NO share) and eat it too (RPL value by big RPL share)
- [support] Universal variable commission
  - This interacts with both of the above to determine where we look good vs competitors (NO-side)
  - There's a lot of room for complication here with PID stuff etc.
  - I'd prefer something very simple: eg, "if DP running weekly average is below X for 2 months,
    decrease commission 1%". It could be executed by security council with something like gate seals
    (eg, 3 one time use 1% moves up or down before pDAO has to vote to refresh their power).
- [support] Protect rETH from outlier bad NOs
  - I think this is quite independent
  - I think this is a lower tier of importance
- [support] Exit validator on ejection balance ~31 ETH
  - I think this is quite independent
  - I think this is a lower tier of importance

While we're at it, some other things that I think are important
- oDAO guardrails from knoshua's work


---
 Ok. Ran the bond curve models:
- 591k      matched_eth
- 942k      matched_eth_current_optimum
- 3.639M    matched_eth_bit_safer
- 5.179M    matched_eth_aggressive_alt
- 5.194M    matched_eth_aggressive
- If we got the matching ETH from rETH, and total staked ETH didn't change at all, these would respectively represent RP dominances of: 2.8%, 4.0%, 12.9%, 18.0%, and 18.0%
- Takeaways:
  - This is massive. Essentially, if we can make this happen, we're realistically in range of our goals.
  - If total staking market increases, we'd need to keep pace or perhaps barely outpace, but not a huge amount.
  - There is little rETH supply difference between aggressive and aggressive alt (and likely other variants like that).

---

I think I want to structure this as:
- Lead actors (bond + value capture)
- Supporting cast
  - UVC with broad heuristic and gate seals
  - Validator ejection based on balance
  - Validator ejection based on sustained bad performance (can we prove balance at a couple points in time to do this?) (metric: performs worse than rETH using CL+smoothed_EL)
  - rETH restitution based on bad performance (ETH rewards, ETH bond)
- The trailer (LEB6, or BPT-backed MYSO loans)
  - Provide a budget for RPL loans (enough for 250 EB8s)
  - Eg start really attractive: 70% LTV, 1 year, 10% up front fee, half of fee is returned if
    - RPL is staked and used to launch minipool(s)
  - Do this in tranches of, eg, 10 EB8 worth. This lets us see if up front fee is enough to avoid
    short sales etc.
- The sequel
  - Moving to direct capture from direct capture 2
  - Automating UVC
  - etc