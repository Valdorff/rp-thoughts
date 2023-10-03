> Vote options:
> - All nodes shall be eligible voters
> - Nodes w/RPL ≥10% borrowed ETH shall be eligible voters
> - Abstain

# Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]

This vote will determine eligible voters for future pDAO governance votes.

There are two concurrent votes to clarify voting criteria:
- `Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]`
- `Clarify Voting Criteria (RPIP-4) [eligible voters: nodes w/RPL ≥10% borrowed ETH]`

These votes are identical except that different strategies were used to determine voter eligibility.

### Context around the situation

RPIP-4 defines who gets to vote: `To be eligible for vote participation, the RPL must be effectively staked in the Rocket Pool protocol as reported by getNodeEffectiveRPLStake().`

This is currently interpreted by people multiple ways, including at least:
- It was meant to be effective stake (10-150%); the function was not there as a definition, but as an implementation that was bugged. Fixing the bugged function (and vote weight) was proper.
- Effective stake is defined in the RPIP using the function at the time. Fixing the bugged function (and vote weight) was inappropriate without pDAO input.
- It's ambiguous.

The voting body _was_ changed with Atlas release - whether that was ok depends on where you land above.
Since this is about voting, we can't do a single vote to figure out what we want -- the set of people that should vote on that is in question (ie, this is a bootstrap problem). This is why the approach is to vote using both possible voting bodies to get this clarified.


### Outcomes
- If both concurrent votes (`Clarify Voting Criteria (RPIP-4) [eligible voters: all nodes]` and `Clarify Voting Criteria (RPIP-4) [eligible voters: nodes w/RPL ≥10% borrowed ETH]`) have matching results, the RPIP Editors are instructed to clarify RPIP-4 and RPIP-8 per those results
  -  Implementation for [eligible voters: all nodes](https://github.com/rocket-pool/RPIPs/pull/86) (commit f0be7ac)
  -  Implementation for [eligible voters: nodes w/RPL ≥10% borrowed ETH](https://github.com/rocket-pool/RPIPs/pull/85) (commit a967777)
- If the votes do not match, or quorum fails on either vote, no action is taken
  - Other votes will remain blocked until a future successful attempt to clarify the voting body


### Further context
- Val suggests a clarification and [polls for overwhelming consensus](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/7) -- it's clear that there's no overwhelming consensus
- Patches suggests the concurrent vote path, which enjoyed strong support in the [poll](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068/41)
- Deep dive:
  - [Full forum thread](https://dao.rocketpool.net/t/rpip-4-effective-rpl-10/2068) that included both of the highlighted posts. Note that the initial topic is slightly different and that incidentally raised this point of ambiguity.
  - Selected discord discussions: [1](https://discord.com/channels/405159462932971535/405163713063288832/1148270849401565315),  [2](https://discord.com/channels/405159462932971535/774497904559783947/1150386963153698898)