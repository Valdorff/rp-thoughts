WITH
  oracle as (
    select
      eth_reth_peg_filled,
      eth_steth_peg_filled,
      eth_cbeth_peg_filled
    from
      query_3303115
    order by
      time desc
    limit
      1
  ),
  reth_supply as (
    select
      reth_supply
    from
      query_1282245
  ),
  cbeth_supply as (
    select
      sum(value) as cbeth_supply
    from
      (
        SELECT
          SUM(value / CAST(1e18 AS DOUBLE)) AS value
        FROM
          evms.erc20_transfers
        WHERE
          contract_address = 0xBe9895146f7AF43049ca1c1AE358B0541Ea49704
          AND "from" = 0x0000000000000000000000000000000000000000
          AND blockchain = 'ethereum'
        UNION ALL
        SELECT
          -1 * SUM(value / CAST(1e18 AS DOUBLE)) AS value
        FROM
          evms.erc20_transfers
        WHERE
          contract_address = 0xBe9895146f7AF43049ca1c1AE358B0541Ea49704
          AND "to" = 0x0000000000000000000000000000000000000000
          AND blockchain = 'ethereum'
      )
  )
  ,
  /* stETH is a rebasing token.  Supply is elastic based on amount of eth staked */
  steth_supply as (
    WITH lido_deposits AS (
    SELECT SUM(cast(value AS DOUBLE))/1e18 AS deposited
    FROM  evms.traces
    WHERE to = 0x00000000219ab540356cbb839cbe05303d7705fa -- beacon contract
      AND blockchain = 'ethereum'
      AND block_time >= CAST('2020-10-01' as timestamp)
      AND call_type = 'call'
      AND success = True 
      AND "from" in (0xae7ab96520de3a18e5e111b5eaab095312d7fe84 --stETH contract
            , 0xB9D7934878B5FB9610B3fE8A5e441e8fad7E293f --withdrawl vault
            , 0xFdDf38947aFB03C621C71b06C9C70bce73f12999) --staking router
    )
     -- This CTE calculates Lido principal withdrawals
    , lido_pricipal_withdrawals AS (
        SELECT 
         (-1) * SUM(CASE WHEN amount BETWEEN 20000000000 AND 32000000000 THEN CAST(amount AS DOUBLE)/1e9 
        WHEN amount > 32000000000 THEN 32 ELSE 0 END) AS withdrawn
        FROM ethereum.withdrawals
        WHERE address = 0xB9D7934878B5FB9610B3fE8A5e441e8fad7E293f --withdrawl vault
        AND amount >= 20000000000 
    )
    -- This CTE retrieves data from query_2481449 ('Lido_buffer') to calculate the most buffer amount for Lido
    , lido_buffer_amount AS (
    SELECT 
      eth_balance as buffer --Lido protocol buffer
    FROM query_2481449 --source is Lido query.  Consider replacing this
    order by time desc 
    limit 1  
    ) 
    -- final query combines all CTEs  
    SELECT 
        deposited,
        buffer,
        withdrawn,
        deposited + buffer + withdrawn AS steth_supply
    FROM lido_deposits
      , lido_buffer_amount
      , lido_pricipal_withdrawals
      )
      
select
  'reth' as lst,
  reth_supply as supply,
  eth_reth_peg_filled as oracle_rate,
  reth_supply * eth_reth_peg_filled as value_eth
from
  reth_supply,
  oracle
UNION
select
  'cbeth' as lst,
  cbeth_supply as supply,
  eth_cbeth_peg_filled as oracle_rate,
  cbeth_supply * eth_cbeth_peg_filled as value_eth
from
  cbeth_supply,
  oracle
 UNION
select
  'steth' as lst,
  steth_supply as supply,
  1 as oracle_rate,
  steth_supply * 1 as value_eth
from
  steth_supply,
  oracle