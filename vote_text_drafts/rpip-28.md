> Vote options:
> - For
> - Against
> - Abstain

# Deposits Under the Minimum (RPIP-28)

RPIP-28 proposes an additional method of creating a new minipool by depositing ETH and RPL together, which will be possible regardless of the Node's current amount of RPL staked.  

### Outcome if vote passes
- RPIP-28 will be implemented in a future smart contract release
- Once implemented, it will be possible to make a minipool deposit when under the "minimum" RPL threshold by depositing the ETH and staking (at least) the minimum amount of RPL needed for a single minipool of that type
  - Note that this new method is in _addition_ to the current method

### Rationale
It is currently possible to create a new node to deposit a minipool. In other words, this feature does _not_ change the ability for a Node Operator to create a new minipool - they'll be able to create one for the same amount of ETH and RPL.

This change instaed makes the process more convenient. A handful of folks have said they would have created more minipool(s) if they could've added them to their existing node while being under the minimum.

This should help us provide more rETH supply, with no significant trade-off.

### Context
- [Full RPIP](https://rpips.rocketpool.net/RPIPs/RPIP-28)
- [Forum thread](https://dao.rocketpool.net/t/allow-minipool-deposits-while-under-min-rpl/2100)

# Rocket Pool Vote Text Checklist
- [x] Vote text should include the following:
  - [x] A short one-line summary intended to display effectively on the snapshot vote-listing page.
  - [x] Context as to the reason for the vote.
  - [x] A clear and concrete explanation of the possible outcomes of the voting process.
  - [x] Links to relevant resources or further context.
  - [x] A link to a relevant discussion thread on the Rocket Pool forums.
- [x] Ensure that all URLs point to the intended destinations.
- [x] Ensure the vote text is presented in a neutral manner.
  - [x] The issue of framing bias has been considered and mitigated where possible.
- [x] RPIP Editors have reviewed vote text.
- [ ] Ensure a relevant representative of Rocket Pool Ltd has approved the vote text.ate in terms of layout.