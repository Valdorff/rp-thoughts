# Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]

There are two concurrent votes:
- `Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]`
- `Clarify Voting Criteria (RPIP-4) [eligible voters: nodes w/RPL ≥10% borrowed ETH]`

These votes have the same text (other than their names) and differ only in how voting eligibility was determined.

### Summary of the situation

RPIP-4, which defines who gets to vote, is currently interpreted by people multiple ways.
There are at least:
- It was meant to be effective stake (10-150%); the function was not there as a definition, but as an implementation that was bugged. Fixing the bugged function (and vote weight) was proper.
- Effective stake is defined in the RPIP using the function at the time. Fixing the bugged function (and vote weight) was inappropriate without pDAO input.
- Effective stake is defined in the RPIP using the function. The function can be changed. Unclear what the end take is, given that there was a change, but the change wasn't pDAO ratified.
- It's ambiguous.

The voting body _was_ changed with Atlas release - whether that was ok depends on where you land above.
Since this is about voting, we can't simply vote to figure out what we want -- the set of people that should vote on that is in question (ie, this is a bootstrap problem). This is why the approach is to vote using both possible voting bodies to get this clarified.

Note: There is no practical way to carry out a vote on initial definition only. That means this vote will determine an _outcome_, so please take that under consideration when selecting your preference. 

### Outcomes
- If both concurrent votes (`Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]` and `Clarify Voting Criteria (RPIP-4) [eligible voters: nodes w/RPL ≥10% borrowed ETH]`) have matching results, the RPIP Editors are instructed to clarify RPIP-4 and RPIP-8 per those results and the `Implementation` section below
- If the votes do not match, or quorum fails on either vote, no action is taken
  - Other votes will remain blocked until a future successful attempt to clarify the voting body

### Implementation

#### Clarify "Implementation" text in RPIP-4
The main clarification, which specifies the set of nodes eligible to receive vote power.
- Current text: `To be eligible for vote participation, the RPL must be effectively staked in the Rocket Pool protocol as reported by getNodeEffectiveRPLStake().`
- Clarify to all nodes eligible: `All nodes are eligible to receive vote power. For nodes eligible to receive vote power, RPL staked on a node contributes to vote power up to 150% of the value of the node's bonded ETH.`
- Clarify to RPL>10% borrowed ETH eligible: `A node is eligible to receive vote power if the RPL staked on it is ≥10% of the value of the node's borrowed ETH. For nodes eligible to receive vote power, RPL staked on a node contributes to vote power up to 150% of the value of the node's bonded ETH.`

#### Clarify "Rationale" text in RPIP-4
Avoid text that could be read as defining things in the Rationale section.
- Current text: `RPL is required to be effectively staked for voting to prevent vote-buying by participants unaffiliated with the protocol’s operations.`
- Clarification: `The RPL eligibility requirements help prevent vote-buying by participants unaffiliated with the protocol’s operations.`

#### Clarify "Specification" text in RPIP-8
There should only be a single source of truth, and this vote will clarify what we want for voting.
- Current text: Effectively staked RPL SHALL be used when calculating RPL rewards and voting power.
- Clarification: Effectively staked RPL SHALL be used when calculating RPL rewards.

### Further context
- Please read:
  - Val suggests a clarification and [polls for overwhelming consensus](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/7?u=valdorff) -- it's clear that there's no overwhelming consensus
  - Patches suggests the concurrent vote path, which enjoyed strong support in the [poll](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/41?u=valdorff)
- [Full forum thread](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068?u=valdorff) that included both of the highlighted posts. Note that the initial topic is slightly different and that incidentally raised this point of ambiguity.
- Selected discord discussions: [1](https://discord.com/channels/405159462932971535/405163713063288832/1148270849401565315),  [2](https://discord.com/channels/405159462932971535/774497904559783947/1150386963153698898)