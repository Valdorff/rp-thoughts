> Vote options:
> - For
> - Against
> - Abstain

This vote aims to align RPL reward spend with rETH capacity created.

### Summary
- RPL rewards will scale differently, with a focus on aligning RPL rewards with supplying rETH
- It will be possible to withdraw down to 15% borrowed ETH
- We will ramp to both of the above states
- Withdrawing will be a 2-step process where RPL is set to "withdrawing" for 28 days before it can
  be withdrawn

### Rationale
The main goal is to align the DAO's spending on RPL rewards with the DAO's goals. In particular, we'll continue to send 70% of inflation to Node Operators, but align it far more with amount of minted rETH.

_Please_ read the Intro document's [context section](https://github.com/Valdorff/rp-thoughts/tree/main/rpl_staking) for a visual representation of spending before and after this change. 

### Detailed Outcomes
- RPL rewards will scale differently
  - Adding a minipool will increase RPL rewards (even if you already had enough staked RPL)
  - Converting an EB16 to two LEB8s will increase rewards (even if you already had enough staked RPL)
  - You need staked RPL value of ≥10% borrowed ETH to get RPL rewards [unchanged]
  - Staking more RPL means more rewards [unchanged], though now without a maximum
  - Beyond 15% borrowed ETH, additional rewards go up slower and slower
  - The rewards changes will be phased in slowly over 6 months
- It will be possible to withdraw down to 15% borrowed ETH
- Make withdrawal a 2-step process
  - Set X RPL to "withdrawing"; these RPL are no longer eligible for rewards or voting 
  - After 28 days, the RPL may be withdrawn
  - Remove the current 28-day withdrawal lock when you stake RPL 
  - Phase in the new rules partially over time, then fully with the next smart contract release
- These changes apply equally to both existing and new NOs

### Context
- [Intro document](https://github.com/Valdorff/rp-thoughts/tree/main/rpl_staking) 
- [Forum thread](https://dao.rocketpool.net/t/rpl-staking-rework-proposal/2090)
- [Full RPIP](https://github.com/rocket-pool/RPIPs/blob/main/RPIPs/RPIP-30.md)
- [Deep dive links](https://github.com/Valdorff/rp-thoughts/tree/main/rpl_staking#what-else-has-been-looked-at-around-this-proposal) (a section within the intro document)

# Rocket Pool Vote Text Checklist
- [ ] Vote text should include the following:
  - [ ] A short one-line summary intended to display effectively on the snapshot vote-listing page.
  - [ ] Context as to the reason for the vote.
  - [ ] A clear and concrete explanation of the possible outcomes of the voting process.
  - [ ] Links to relevant resources or further context.
  - [ ] A link to a relevant discussion thread on the Rocket Pool forums.
- [ ] Ensure that all URLs point to the intended destinations.
- [ ] Ensure the vote text is presented in a neutral manner.
  - [ ] The issue of framing bias has been considered and mitigated where possible.
- [ ] RPIP Editors have reviewed vote text.
- [ ] Ensure a relevant representative of Rocket Pool Ltd has approved the vote text.ate in terms of layout.