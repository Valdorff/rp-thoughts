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
      AND (token_bought_address = 0xae78736Cd615f374D3085123A210448E74Fc6393
      OR token_sold_address = 0xae78736Cd615f374D3085123A210448E74Fc6393)
      AND block_time >= CAST('2022-01-01' AS TIMESTAMP)
      AND tx_hash != 0xe18c205f50edd71c64fd8584f5e148d22fb3847428a877bcc50e26d1a89be13f -- Remove an outlier transaction
      AND tx_hash != 0x68f4a987b11d264b079ca4570e7e528519fe0847993deeeded838ca56ba5b64e -- Remove an outlier transaction
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
        WHEN token_bought_address = 0xae7ab96520de3a18e5e111b5eaab095312d7fe84 THEN token_bought_amount
        ELSE token_sold_amount
      END AS steth_amount,
      amount_usd
    FROM
      dex.trades
    WHERE
      blockchain = 'ethereum'
      AND (token_bought_address = 0xae7ab96520de3a18e5e111b5eaab095312d7fe84
      OR token_sold_address = 0xae7ab96520de3a18e5e111b5eaab095312d7fe84)
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
  cbeth_trades AS (
    SELECT
      block_time AS time,
      CASE
        WHEN token_bought_address = 0xBe9895146f7AF43049ca1c1AE358B0541Ea49704 THEN token_bought_amount
        ELSE token_sold_amount
      END AS cbeth_amount,
      amount_usd
    FROM
      dex.trades
    WHERE
      blockchain = 'ethereum'
      AND (token_bought_address = 0xBe9895146f7AF43049ca1c1AE358B0541Ea49704
      OR token_sold_address = 0xBe9895146f7AF43049ca1c1AE358B0541Ea49704)
      AND block_time >= CAST('2022-01-01' AS TIMESTAMP)
  ),
  cbeth_trades_eth_amount AS (
    SELECT
      t.time,
      t.cbeth_amount,
      t.amount_usd / CAST(p.price AS DOUBLE) AS eth_amount /* Trade size in USD divided by USD/ETH is amount of USD. */
    FROM
      cbeth_trades AS t
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
    SELECT *, "totalEth" / CAST("rethSupply" AS DOUBLE) AS eth_reth_peg from reth_evt_preatlas
    UNION
    SELECT *, "totalEth" / CAST("rethSupply" AS DOUBLE) AS eth_reth_peg from reth_evt_atlas
    ORDER BY referenceBlock ASC
  ),

  -- The 3 subtables above com from https://dune.com/queries/1916466/3189364 and give us a valid event across upgrades
    cbeth_evt as (
    SELECT
    CAST(evt_block_number as bigint) as block,
    evt_block_time as time,
    cast(newExchangeRate as double)/1e18 AS eth_cbeth_peg
    FROM coinbase_ethereum.StakedTokenV1_evt_ExchangeRateUpdated
    WHERE evt_block_time >= cast('2022-07-15 00:00' as timestamp)
    ORDER BY time ASC
    ),

    cb_reth_unified as 
    (SELECT
      COALESCE(CAST(referenceBlock as bigint),cb.block) as block,
      eth_reth_peg,
      eth_cbeth_peg
    FROM
      reth_evt_unified r
      FULL OUTER JOIN cbeth_evt cb on cb.block = CAST(r.referenceBlock as bigint)
    WHERE
      CAST(referenceBlock as bigint) > 13578840
      OR cb.block > 13578840
    ORDER BY 1 asc
    ),

  balances_updated
  AS (
    SELECT
      block,
      /* Pegs exist at different blocks.  Use previous peg if a value does not exist for that block */
      COALESCE(eth_reth_peg, LAG(eth_reth_peg,1) over (order by block asc), LAG(eth_reth_peg,2) over (order by block asc)) as eth_reth_peg, 
      COALESCE(eth_cbeth_peg, LAG(eth_cbeth_peg,1) over (order by block asc),LAG(eth_cbeth_peg,2) over (order by block asc)) as eth_cbeth_peg

    FROM
      cb_reth_unified
    WHERE
      block > 13578840
  ),
  peg AS (
    SELECT
      time,
      d.eth_reth_peg,
      d.eth_cbeth_peg
    FROM
      blocks AS b
      JOIN balances_updated AS d ON b.block = d.block
      INNER JOIN reth_evt_unified r on r.referenceBlock = b.block /* this limits pegs to only rETH reported blocks.  
      If you remove this it will also show values for cbETH oracle blocks and prices will vary for each interval based on makeup of swaps */
  ),
  joined AS (
    SELECT
      COALESCE(r.time, s.time, p.time) AS time,
      r.reth_amount,
      r.eth_amount,
      s.steth_amount,
      s.eth_amount AS eth_amount_for_steth,
      c.cbeth_amount,
      c.eth_amount AS eth_amount_for_cbeth,
      p.eth_reth_peg,
      p.eth_cbeth_peg
    FROM
      reth_trades_eth_amount AS r
      FULL OUTER JOIN steth_trades_eth_amount AS s ON r.time = s.time
      FULL OUTER JOIN cbeth_trades_eth_amount AS c ON r.time = c.time
      FULL OUTER JOIN peg AS p ON r.time = p.time
  ),
  back_filled AS (
    SELECT
      MAX(time) AS time,
      SUM(eth_amount) / CAST(SUM(reth_amount) AS DOUBLE) AS eth_reth_price,
      SUM(eth_amount_for_steth) / CAST(SUM(steth_amount) AS DOUBLE) AS eth_steth_price,
      MAX(eth_reth_peg) AS eth_reth_peg,
      MAX(eth_cbeth_peg) AS eth_cbeth_peg,
      /* There is only one non-null peg price per group, so use max to snag it. */ SUM(eth_amount) / SUM(reth_amount) / CAST(MAX(eth_reth_peg) AS DOUBLE) AS reth_price_peg_ratio,
      SUM(eth_amount_for_cbeth) / SUM(cbeth_amount) / CAST(MAX(eth_cbeth_peg) AS DOUBLE) AS cbeth_price_peg_ratio
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
  (cbeth_price_peg_ratio - 1) AS cbeth_peg_pct_divergence,
  (eth_steth_price - 1) AS steth_peg_pct_divergence
FROM
  back_filled
WHERE
  NOT reth_price_peg_ratio IS NULL /* Drop the most recent data until the peg is reported. */
   AND (eth_reth_peg != 1.0775370240180655)  -- filter out one bad day of market data caused by games on a curve pool
