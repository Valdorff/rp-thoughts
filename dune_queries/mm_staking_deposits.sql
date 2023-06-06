WITH
  transactions as (
    SELECT
      *
    FROM
      ethereum.transactions
    WHERE
      block_time >= TIMESTAMP '2023-02-01'
  ),
  mm_deposits as (
    SELECT
      *,
      'Lido' as deposit_type
    FROM
      metamask_ethereum.StakingAggregator_call_depositToLido
    UNION
    SELECT
      *,
      'RP' as deposit_type
    FROM
      metamask_ethereum.StakingAggregator_call_depositToRP
  ),
  combined as (
    SELECT
      block_time,
      block_number,
      value / 1e18 as value,
      deposit_type,
      DATE(block_time) as deposit_date
    FROM
      transactions
      INNER JOIN mm_deposits ON transactions.hash = mm_deposits.call_tx_hash
    WHERE
      success = true
    ORDER by
      block_time desc
  ),
  per_day as (
    SELECT
      deposit_date,
      deposit_type,
      SUM(value) as deposits
    FROM
      combined
    GROUP BY
      deposit_date,
      deposit_type
  )
SELECT
  *
FROM
  per_day
ORDER BY
  deposit_date desc