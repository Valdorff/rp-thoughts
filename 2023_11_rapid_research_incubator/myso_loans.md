This idea is meant to address "Rapid Research Incubator" topic #2 and, to a lesser degree #1
  - #2 alternative value capture for RPL: while the bond remains the core value capture, smoothing the path for loans provides a way for RPL to create value for a holder without needing to personally run a node
  - #1 helps balance supply/demand between RPL holders and NOs: the loan price can be responsive -- if many NOs are looking to borrow RPL at the current loan price, lenders can increase the price. In this case, that transfers value from NOs to RPL holders (or the subset of them that are lenders anyhow). On the flip side, if few NOs are looking to borrow at current loan terms, lenders can compete on price to attract borrowers.

## The general idea
- We modify the required RPL bond as needed to hit the desired NO vs protocol split
  - As an estimate, the equivalent "protocol fee" is `required_RPL_bond_value_in_eth/ETH_borrowed`
    - TODO: refine this to be correct rather than estimated - we saw math wasn't exact
  - The "NO fee" is then `commission - protocol fee`
  - There are simplifications, but a start
- We do not support ETHless minipools in protocol, but we facilitate a third-party lender that works well for this use case

## Lending
The logical lender in mye eyes is MYSO right now.
Their offering is liquidation-free loans with an upfront fee, which allows them to support (a) long
tenors such as two years and (b) calculable costs.

One concern here is that loans need not be used for running minipools:
- We could create some smart contracts to force that usage - this is fairly complex but possible
- We could have loans with bad rates (eg, double the desired rate) that get a retrospective award if they are used in a way we "support"
  - Eg, all borrowed RPL must be staked
  - Once staked, at least the amount of RPL borrowed must stay staked for at least the full tenor minus one month
  - The loan is repaid
  - If the above happens, the GMC refunds part of the upfront loan to make it a good deal
  - (obviously, half the upfront fee would need to go to a GMC-controlled address here, and we'd need some scripts to make determining payouts etc painless)

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
- Let's 
- We should have RP team look at audits etc and changes since then. We also need some understanding of offchain components. If we have uncertainty, there's a potential need to fund an audit.
- RPL slashing can occur as effectively as for a node without loaned RPL -- they need to pay back, so slashing is meaningful and there's no principal agent problem
  - While the adder is very small, the fee repayment could also be slashed in theory
- A possible extension would be using the rETH from the upfront fees that we plan to refund for protocol owned liquidity

## Pros/Cons vs other thoughts
- Pro: keeps changes minimal -- in fact, there are no smart contract changes needed
- Pro: The market can reward RPL holders (that lend) based on what fees NOs are willing to pay -- this can even handle complex things like RPL APR attractiveness
- Con: Can't use the collateral for staking, so some inefficiency in holding rETH
- Con: Can't use 100% LTV safely, so more inefficiency from holding more collateral
- 
