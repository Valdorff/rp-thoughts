# Clarify Voting Criteria (RPIP-4) [0-150% strategy]

### Summary of the situation

RPIP-4, which defines who gets to vote, is currently interpreted by people multiple ways.
There are at least:
- It was meant to be effective stake (10-150%); the function was not there as a definition, but as an implementation that was bugged. Fixing the bugged function (and vote weight) is proper.
- Effective stake is defined in the RPIP using the function at the time. Fixing the bugged function (and vote weight) was inappropriate without pDAO input.
- Effective stake is defined in the RPIP using the function. The function can be changed. Unclear what the end take is, given that there was a change, but the change wasn't pDAO ratified.
- It's ambiguous.

The voting body _was_ changed with Atlas release - whether that was ok depends on where you land above.
Since this is about voting, we can't simply vote to figure out what we want -- the set of people that should vote on that is in question (ie, this is a bootstrap problem). This is why the approach is to vote using both possible voting bodies to get this clarified.

### Outcomes
- If both this vote and the concurrent `Clarify Voting Criteria (RPIP-4) [10-150% strategy]` votes have matching results, the RPIP Editors are instructed to clarify RPIP-4 per those results
- If the votes do not match, or quorum fails on either vote, no action is taken and other votes will remain blocked until a future successful attempt to clarify RPIP-4

### Implementation

#### Clarify "Implementation" text
- Current text: `To be eligible for vote participation, the RPL must be effectively staked in the Rocket Pool protocol as reported by getNodeEffectiveRPLStake().`
- Clarify to 0-150%: `RPL staked on a node contributes to vote power up to 150% of the value of the node's bonded ETH.`
- Clarify to 10-150%: `A node is eligible to get vote power if the RPL staked on it is ≥10% of the value of the node's borrowed ETH. For nodes eligible to receive vote power, RPL staked on a node contributes to vote power up to 150% of the value of the node's bonded ETH.`

#### Clarify "Rationale" text
- Current text: `RPL is required to be effectively staked for voting to prevent vote-buying by participants unaffiliated with the protocol’s operations.`
- Clarification: `The RPL eligibility requirements help prevent vote-buying by participants unaffiliated with the protocol’s operations.`

### Further context
- Please read:
  - Val suggests a clarification and [polls for overwhelming consensus](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/7?u=valdorff) -- it's clear that there's no overwhelming consensus
  - Patches suggests the concurrent vote path, which enjoyed strong support in the [poll](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/41?u=valdorff)
- [Full forum thread](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068?u=valdorff) that included both of the highlighted posts. Note that the initial topic is slightly different and that incidentally raised this point of ambiguity.
- Selected discord discussions: [1](https://discord.com/channels/405159462932971535/405163713063288832/1148270849401565315),  [2](https://discord.com/channels/405159462932971535/774497904559783947/1150386963153698898)