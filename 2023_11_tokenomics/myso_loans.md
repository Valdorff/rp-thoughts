The premise of this idea is to (a) keep change minimal and (b) let the markets figure out pricing.

Let's start by explaining the idea, and then trying to put numbers to it.

## The general idea
- We modify the required RPL bond as needed to hit the desired NO vs protocol split
  - As an estimate, the equivalent "protocol fee" is `required_RPL_bond_value_in_eth/ETH_borrowed`
    - TODO: refine this to be correct rather than estimated - we saw math wasn't exact
  - The "NO fee" is then `commission - protocol fee`
  - There are simplifications, but a start
- We do not support ETHless minipools in protocol, but we facilitate a third-party lender that works well for this use case

## Lending
The logical lender to me is MYSO right now.
Their offering is liquidation-free loans with an upfront fee, which allows them to support (a) long
tenors such as two years and (b) calculable costs.
One concern here is that loans need not be used for running minipools:
- We could create some smart contracts to force that usage - this is fairly complex but possible
- We could have loans with bad rates (eg, double the desired rate) that get a retrospective award if they are used in a way we like
  - Eg, all borrowed RPL must be staked
  - Once staked, all borrowed RPL must stay staked for at least the full tenor minus one month
  - The loan is repaid
  - If the above happens, the GMC refunds part of the upfront loan to make it a good deal
  - (obviously, half the upfront fee would need to go to a GMC-controlled address here, and we'd need some scripts to make this painless)

## Valuation
This doesn't affect valuation from current modeling. Insofar as the bond is modified, that term gets modified.

The loaning aspect has no direct impact. If successful, it has an indirect impact via growth.

## Thoughts
- What if there isn't a price point where lenders and borrowers agree?
  - This can happen if the lenders are all more bullish than the borrowers, eg.
  - MYSO does have tools using black-sholes to get to a realistic price.
  - If they really can't agree... lowering the bond required could work? That would "damage" RPL value per TVL and thus maybe close the gap?
- Collateral means inefficiency, especially at lower LTV; this can be minimized by using rETH collateral, but not eliminated
  - For current LEB8s, your apr calc is currently `solo*(8+2.4*.14)/(8+2.4) = solo*1.092`
  - With rETH collateral at 100% LTV, we'd have `solo*(8+2.4*.14+2.4*.86)/(8+2.4) = solo*1.29` before loan fees
  - With rETH collateral at 50% LTV, we'd have `solo*(8+2.4*.14+4.8*.86)/(8+4.8) = solo*1.21` before loan fees
  - With rETH collateral at 33% LTV, we'd have `solo*(8+2.4*.14+7.2*.86)/(8+7.2) = solo*1.15` before loan fees
- We should have RP team look at audits etc and changes since then. We also need some understanding of offchain components. If we have uncertainty, there's a potential need to fund an audit.