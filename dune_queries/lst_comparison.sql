-- Used for:
--     Trailing month APY line chart
--     Trailing week APY line chart
--     Single update APY line chart
--     rETH/stETH/cbETH post-merge average number
--     Oracle rate chart
--     APY table with columns: time, rETH APY, stETH APY, cbETH APY, rETH APY (~7.2d),
--         stETH APY (7d), cbETH APY (7d), rETH APY (~30.4d), stETH APY (30d),
--         cbETH APY (30d), eth_reth_peg_filled, eth_cbeth_peg_filled

WITH
-- rETH
blocks AS (
    SELECT
    time,
    cast("number" as uint256) AS block
    FROM ethereum.blocks
    WHERE "number" > 13578840
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
    and block_time >= cast('2023-04-08 00:00' as timestamp)
    AND topic0 = 0x7bbbb137fdad433d6168b1c75c714c72b8abe8d07460f0c0b433063e7bf1f394
    ORDER BY referenceBlock ASC
),

reth_evt_houston as (
    select
        block_time as evt_block_time,
        block_number as evt_block_number,
        bytearray_to_uint256(topic1) as referenceBlock,
        bytearray_to_uint256(bytearray_substring(data, 33, 32)) as totalEth,
        bytearray_to_uint256(bytearray_substring(data, 97, 32)) as rethSupply
    from
        ethereum.logs
    where
        contract_address = 0x6cc65bf618f55ce2433f9d8d827fc44117d81399
        and block_time >= cast('2024-06-18 00:00' as timestamp)
        and topic0 = 0xdd27295717c4fbd48b1840f846e18be6f0b7bd6b55608e697e53b15848cecdf9
    ORDER BY referenceBlock ASC
),

reth_evt_unified AS (
    SELECT * from reth_evt_preatlas
    UNION
    SELECT * from reth_evt_atlas
    UNION
    SELECT * from reth_evt_houston
    ORDER BY referenceBlock ASC
),

reth_evt_unifiedwithreftime AS (
    SELECT
    evt_block_time,
    evt_block_number,
    to_unixtime(time) as referenceTime,
    totalEth,
    rethSupply
    FROM blocks b
    JOIN reth_evt_unified r
    ON b.block = r.referenceBlock
),

reth_evt AS (
    SELECT
    evt_block_time,
    evt_block_number,
    referenceTime,
    referenceTime - NULLIF(coalesce(lag(referenceTime) over (order by referenceTime), 0), 0) as timeSinceLastUpdate,
    totalEth,
    cast(totalEth as double) / cast(rethSupply as double) AS eth_reth_peg
    FROM reth_evt_unifiedwithreftime
),

reth AS (
    SELECT
    evt_block_time,
    evt_block_number,
    referenceTime,
    eth_reth_peg,
    -- 365*24*60*60=31536000 seconds in a year
    100 * (31536000 / cast(timeSinceLastUpdate as double)) * (eth_reth_peg/NULLIF(coalesce(lag(eth_reth_peg) over (order by referenceTime), 0), 0) - 1) as apy
    FROM reth_evt
),

reth_avg AS (
    SELECT
    evt_block_time,
    evt_block_number,
    referenceTime,
    eth_reth_peg,
    apy as "rETH APY",
    AVG(apy) OVER (ORDER BY evt_block_time ASC ROWS BETWEEN 8 PRECEDING AND CURRENT ROW) as "rETH APY (~7.2d)",
    AVG(apy) OVER (ORDER BY evt_block_time ASC ROWS BETWEEN 37 PRECEDING AND CURRENT ROW) as "rETH APY (~30.4d)"
    FROM reth
    WHERE evt_block_number != 15891919 -- remove a high apy caused by a bugfix accounting for some ETH that hadn't been getting counted
),

-- stETH; adapted from https://dune.com/queries/570874/1068499
-- This CTE calculates pre AND post share rates for the stETH
steth_shares AS (
SELECT
  preTotalEther * 1e27 / preTotalShares AS pre_share_rate,
  postTotalEther * 1e27 / postTotalShares AS post_share_rate,
  *
FROM
  lido_ethereum.steth_evt_TokenRebased
),

-- This CTE combines data from the legacy oracle end the new V2 oracle, calculating APR values
steth_evt AS (
--legacy oracle
SELECT
  "evt_block_time" AS time,
  cast(("postTotalPooledEther" - "preTotalPooledEther") * 365 * 24 * 60 * 60 / ("preTotalPooledEther") AS double) / timeElapsed * 0.9 * 100 AS "apy",
  "postTotalPooledEther"/cast(totalShares as double) as eth_steth_peg
FROM
  lido_ethereum.LegacyOracle_evt_PostTotalShares
WHERE
  "evt_block_time" >= cast('2022-09-01 00:00' AS TIMESTAMP)
  AND "evt_block_time" <= cast('2023-05-16 00:00' AS TIMESTAMP)
--new V2 oracle
UNION all
SELECT
  "evt_block_time" AS time,
  365 * 24 * 60 * 60 * (post_share_rate - pre_share_rate) / pre_share_rate / timeElapsed * 100 AS "apy",
  NULL as eth_steth_peg
FROM
  steth_shares
),

steth_peg AS (
  SELECT
    call_block_time as time,
    cast(json_extract_scalar(data, '$.simulatedShareRate') as double)/1e27 as eth_steth_peg
  FROM lido_ethereum.AccountingOracle_call_submitReportData
  WHERE call_success = true
    AND call_block_time > cast('2023-05-16 00:00' as timestamp)
),

steth_preavg AS (
    SELECT
        time,
        apy as "stETH APY",
        AVG(apy) OVER (ORDER BY steth_evt.time ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as "stETH APY (7d)",
        AVG(apy) OVER (ORDER BY steth_evt.time ASC ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as "stETH APY (30d)",
        eth_steth_peg
    FROM steth_evt
),

steth_avg AS (
    SELECT
        COALESCE(steth_preavg.time, steth_peg.time) AS time,
        "stETH APY",
        "stETH APY (7d)",
        "stETH APY (30d)",
        COALESCE(steth_preavg.eth_steth_peg, steth_peg.eth_steth_peg) as eth_steth_peg
    FROM steth_preavg
    FULL OUTER JOIN steth_peg ON steth_peg.time = steth_preavg.time
),

-- cbETH
cbeth_evt AS (
    SELECT
    evt_block_number,
    evt_block_time as time,
    cast(newExchangeRate as double)/1e18 AS eth_cbeth_peg
    FROM coinbase_ethereum.StakedTokenV1_evt_ExchangeRateUpdated
    WHERE evt_block_time >= cast('2022-07-15 00:00' as timestamp)
    ORDER BY time ASC
),

cbeth AS (
    SELECT
    time,
    evt_block_number,
    eth_cbeth_peg,
    -- Daily update
    100* 365 * ((eth_cbeth_peg/NULLIF(coalesce(lag(eth_cbeth_peg) over (order by time), 0), 0)-1)) as apy
    FROM cbeth_evt
),

cbeth_avg AS (
    SELECT
    time,
    evt_block_number,
    eth_cbeth_peg,
    apy as "cbETH APY",
    AVG(apy) OVER (ORDER BY time ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as "cbETH APY (7d)",
    AVG(apy) OVER (ORDER BY time ASC ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) as "cbETH APY (30d)"
    FROM cbeth
),

-- APY since merge
-- First update 9-15-2022 or later: reth=15540507, cbeth=15540147, steth=15539081
-- TODO -- add this. Should be easy for the ones with a peg; not sure what I'd do for steth yet

-- putting it all together
combined AS (
    SELECT
    COALESCE(reth_avg.evt_block_time, steth_avg.time, cbeth_avg.time) AS time,
    COALESCE(reth_avg.evt_block_number, cbeth_avg.evt_block_number) AS block,
    "rETH APY",
    "stETH APY",
    "cbETH APY",
    "rETH APY (~7.2d)",
    "stETH APY (7d)",
    "cbETH APY (7d)",
    "rETH APY (~30.4d)",
    "stETH APY (30d)",
    "cbETH APY (30d)",
    eth_reth_peg,
    eth_cbeth_peg,
    eth_steth_peg
    FROM reth_avg
    FULL OUTER JOIN steth_avg ON steth_avg.time = reth_avg.evt_block_time
    FULL OUTER JOIN cbeth_avg ON cbeth_avg.time = reth_avg.evt_block_time
),

ffill_helper AS (
    SELECT
    time,
    eth_reth_peg,
    eth_cbeth_peg,
    eth_steth_peg,
    count(eth_reth_peg) OVER (ORDER BY time) AS eth_reth_peg_group,
    count(eth_cbeth_peg) OVER (ORDER BY time) AS eth_cbeth_peg_group,
    count(eth_steth_peg) OVER (ORDER BY time) AS eth_steth_peg_group
    FROM combined
),

ffilled AS (
    SELECT
    time,
    coalesce(eth_reth_peg, first_value(eth_reth_peg) OVER (partition by eth_reth_peg_group ORDER BY time)) as eth_reth_peg_filled,
    coalesce(eth_cbeth_peg, first_value(eth_cbeth_peg) OVER (partition by eth_cbeth_peg_group ORDER BY time)) as eth_cbeth_peg_filled,
    coalesce(eth_steth_peg, first_value(eth_steth_peg) OVER (partition by eth_steth_peg_group ORDER BY time)) as eth_steth_peg_filled
    FROM ffill_helper
),

postmerge AS (
    SELECT
    COALESCE(ffilled.time, combined.time) AS time,
    block,
    "rETH APY",
    "stETH APY",
    "cbETH APY",
    "rETH APY (~7.2d)",
    "stETH APY (7d)",
    "cbETH APY (7d)",
    "rETH APY (~30.4d)",
    "stETH APY (30d)",
    "cbETH APY (30d)",
    eth_reth_peg_filled,
    eth_cbeth_peg_filled,
    eth_steth_peg_filled
    FROM combined
    FULL OUTER JOIN ffilled ON ffilled.time = combined.time
    WHERE combined.time >= cast('2022-09-15 00:00' as timestamp)
),

avg_postmerge AS (
  SELECT
  MAX(time) as time,
  AVG("rETH APY") as "rETH APY (since merge)",
  AVG("stETH APY") as "stETH APY (since merge)",
  AVG("cbETH APY") as "cbETH APY (since merge)"
  FROM postmerge
),

display AS (
    SELECT COALESCE(avg_postmerge.time, postmerge.time) AS time,
    block,
    "rETH APY",
    "stETH APY",
    "cbETH APY",
    "rETH APY (~7.2d)",
    "stETH APY (7d)",
    "cbETH APY (7d)",
    "rETH APY (~30.4d)",
    "stETH APY (30d)",
    "cbETH APY (30d)",
    eth_reth_peg_filled,
    eth_cbeth_peg_filled,
    eth_steth_peg_filled,
    "rETH APY (since merge)",
    "stETH APY (since merge)",
    "cbETH APY (since merge)"
    FROM postmerge
    FULL OUTER JOIN avg_postmerge ON avg_postmerge.time = postmerge.time
)

SELECT
*
FROM display
ORDER BY time DESC

-- colors for lines: rETH FD7861, stETH 00A3FF, cbETH 0052FF