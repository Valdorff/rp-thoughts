-- TODO; there seem to be spikes on some days that are unlikely to be real; need to track down n fix the artifact

-- Used for:
--     Percent Discount (negative) or Premium (positive); line chart showing reth_peg_pct_divergence and steth_peg_pct_divergence
--     rETH Exchange Rate Over Time; line chart showing NAV rate and market rate
--     rETH Discount (-) or Premium (+); counter showing reth_peg_pct_divergence to 4 decimals

/* The Rocket Pool oDAO reports the protocol balances every 19.2 hours which forms the rETH peg price. */
/* This table has one row per peg price update, which includes: */
/* - rETH peg price as reported by Rocket Pool oDAO */
/* - Market price of rETH for the reporting period immediately preceeding the rETH peg price update. This is a volume-weighted average price (VWAP) over the period. */
/* - Market price of stETH for the same period. */
WITH
  reth_trades AS (
    SELECT
      block_time AS time,
      CASE
        WHEN token_bought_address = 0xae78736Cd615f374D3085123A210448E74Fc6393 THEN token_bought_amount
        ELSE token_sold_amount
      END AS reth_amount,
      amount_usd
    FROM
      dex.trades
    WHERE
      blockchain = 'ethereum'
      AND token_bought_address = 0xae78736Cd615f374D3085123A210448E74Fc6393
      OR token_sold_address = 0xae78736Cd615f374D3085123A210448E74Fc6393
      AND block_time >= CAST('2022-01-01' AS TIMESTAMP)
  ),
  reth_trades_eth_amount AS (
    SELECT
      t.time,
      t.reth_amount,
      t.amount_usd / CAST(p.price AS DOUBLE) AS eth_amount /* Trade size in USD divided by USD/ETH is amount of USD. */
    FROM
      reth_trades AS t
      JOIN prices.usd AS p ON p.minute = DATE_TRUNC('minute', t.time)
      AND p.symbol = 'WETH'
      AND NOT t.amount_usd IS NULL /* We need to drop trades if the ETH amount will be unknown. This drops the rETH/RPL pair since USD amount is not reported. */
      AND NOT p.price IS NULL
      AND p.price > 0
    WHERE
      p.blockchain = 'ethereum'
  ),
  steth_trades AS (
    SELECT
      block_time AS time,
      CASE
        WHEN token_bought_symbol = 'stETH' THEN token_bought_amount
        ELSE token_sold_amount
      END AS steth_amount,
      amount_usd
    FROM
      dex.trades
    WHERE
      blockchain = 'ethereum'
      AND token_bought_address = 0xae7ab96520de3a18e5e111b5eaab095312d7fe84
      OR token_sold_address = 0xae7ab96520de3a18e5e111b5eaab095312d7fe84
      AND block_time >= CAST('2022-01-01' AS TIMESTAMP)
  ),
  steth_trades_eth_amount AS (
    SELECT
      t.time,
      t.steth_amount,
      t.amount_usd / CAST(p.price AS DOUBLE) AS eth_amount /* Trade size in USD divided by USD/ETH is amount of USD. */
    FROM
      steth_trades AS t
      JOIN prices.usd AS p ON p.minute = DATE_TRUNC('minute', t.time)
      AND p.symbol = 'WETH'
      AND NOT t.amount_usd IS NULL /* We need to drop trades if the ETH amount will be unknown. */
      AND NOT p.price IS NULL
      AND p.price > 0
    WHERE
      p.blockchain = 'ethereum'
  ),
  blocks /* rETH peg query is copied from https://dune.com/queries/1285810. */ AS (
    SELECT
      time,
      "number" AS block
    FROM
      ethereum.blocks
    WHERE
      "number" > 13578840
  ),

  reth_evt_preatlas AS (
    SELECT
    evt_block_time,
    evt_block_number,
    block as referenceBlock,
    totalEth,
    rethSupply
    FROM rocketnetwork_ethereum.RocketNetworkBalances_evt_BalancesUpdated
    WHERE evt_block_time >= cast('2022-07-15 00:00' as timestamp)
    ORDER BY referenceBlock ASC
  ),

  reth_evt_atlas AS (
    -- Grab BalancesUpdated(_block, _totalEth, _stakingEth, _rethSupply, block.timestamp);
    SELECT
    block_time as evt_block_time,
    block_number as evt_block_number,
    bytearray_to_uint256(bytearray_substring(data, 1, 32)) as referenceBlock,
    bytearray_to_uint256(bytearray_substring(data, 33, 32)) as totalEth,
    bytearray_to_uint256(bytearray_substring(data, 97, 32)) as rethSupply
    FROM ethereum.logs
    WHERE contract_address = 0x07FCaBCbe4ff0d80c2b1eb42855C0131b6cba2F4
    AND topic0 = 0x7bbbb137fdad433d6168b1c75c714c72b8abe8d07460f0c0b433063e7bf1f394
    ORDER BY referenceBlock ASC
  ),

   reth_evt_unified AS (
    SELECT * from reth_evt_preatlas
    UNION
    SELECT * from reth_evt_atlas
    ORDER BY referenceBlock ASC
  ),

  -- The 3 subtables above com from https://dune.com/queries/1916466/3189364 and give us a valid event across upgrades
  balances_updated
  AS (
    SELECT
      CAST(referenceBlock as bigint) as block,
      "totalEth" / CAST("rethSupply" AS DOUBLE) AS eth_reth_peg
    FROM
      reth_evt_unified
    WHERE
      CAST(referenceBlock as bigint) > 13578840
  ),
  peg AS (
    SELECT
      time,
      eth_reth_peg
    FROM
      blocks AS b
      JOIN balances_updated AS d ON b.block = d.block
  ),
  joined AS (
    SELECT
      COALESCE(r.time, s.time, p.time) AS time,
      r.reth_amount,
      r.eth_amount,
      s.steth_amount,
      s.eth_amount AS eth_amount_for_steth,
      p.eth_reth_peg
    FROM
      reth_trades_eth_amount AS r
      FULL OUTER JOIN steth_trades_eth_amount AS s ON r.time = s.time
      FULL OUTER JOIN peg AS p ON r.time = p.time
  ),
  back_filled AS (
    SELECT
      MAX(time) AS time,
      SUM(eth_amount) / CAST(SUM(reth_amount) AS DOUBLE) AS eth_reth_price,
      SUM(eth_amount_for_steth) / CAST(SUM(steth_amount) AS DOUBLE) AS eth_steth_price,
      MAX(eth_reth_peg) AS eth_reth_peg,
      /* There is only one non-null peg price per group, so use max to snag it. */ SUM(eth_amount) / SUM(reth_amount) / CAST(MAX(eth_reth_peg) AS DOUBLE) AS reth_price_peg_ratio,
      SUM(eth_amount) / SUM(reth_amount) / CAST(MAX(eth_reth_peg) AS DOUBLE) AS reth_price_peg_pct
    FROM
      (
        SELECT
          *,
          COUNT(eth_reth_peg) OVER (
            ORDER BY
              time DESC
          ) AS peg_group
        FROM
          joined
      ) AS g
    GROUP BY
      peg_group
    ORDER BY
      time DESC
  )
SELECT
  *,
  eth_reth_peg as "NAV rate (aka primary, peg, burn/mint)",
  eth_reth_price as "Market rate (aka secondary)",
  (reth_price_peg_ratio - 1) AS reth_peg_pct_divergence,
  (eth_steth_price - 1) AS steth_peg_pct_divergence
FROM
  back_filled
WHERE
  NOT reth_price_peg_ratio IS NULL /* Drop the most recent data until the peg is reported. */