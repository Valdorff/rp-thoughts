-- !! Uses deprecated dune engine

-- The Rocket Pool oDAO reports the protocol balances every 19.2 hours which forms the rETH peg price.
-- This table has one row per peg price update, which includes:
-- - rETH peg price as reported by Rocket Pool oDAO
-- - Market price of rETH for the reporting period immediately preceeding the rETH peg price update. This is a volume-weighted average price (VWAP) over the period.
-- - Market price of stETH for the same period.

WITH reth_trades AS (
    SELECT
        block_time AS time,
        CASE WHEN token_a_symbol = 'rETH' THEN token_a_amount ELSE token_b_amount END AS reth_amount,
        usd_amount
    FROM dex.trades
    WHERE token_a_symbol = 'rETH' OR token_b_symbol = 'rETH'
    AND category = 'DEX'
    AND block_time >= '2022-01-01'
),

reth_trades_eth_amount AS (
    SELECT
        t.time,
        t.reth_amount,
        t.usd_amount / p.price AS eth_amount  -- Trade size in USD divided by USD/ETH is amount of USD.
    FROM reth_trades t
    JOIN prices.usd p
    ON p.minute = DATE_TRUNC('minute', t.time)
    AND p.symbol = 'WETH'
    -- We need to drop trades if the ETH amount will be unknown. This drops the rETH/RPL pair since USD amount is not reported.
    AND t.usd_amount IS NOT NULL
    AND p.price IS NOT NULL
    AND p.price > 0
),

steth_trades AS (
    SELECT
        block_time AS time,
        CASE WHEN token_a_symbol = 'stETH' THEN token_a_amount ELSE token_b_amount END AS steth_amount,
        usd_amount
    FROM dex.trades
    WHERE token_a_symbol = 'stETH' OR token_b_symbol = 'stETH'
    AND category = 'DEX'
    AND block_time >= '2022-01-01'
),

steth_trades_eth_amount AS (
    SELECT
        t.time,
        t.steth_amount,
        t.usd_amount / p.price AS eth_amount  -- Trade size in USD divided by USD/ETH is amount of USD.
    FROM steth_trades t
    JOIN prices.usd p
    ON p.minute = DATE_TRUNC('minute', t.time)
    AND p.symbol = 'WETH'
    -- We need to drop trades if the ETH amount will be unknown.
    AND t.usd_amount IS NOT NULL
    AND p.price IS NOT NULL
    AND p.price > 0
),

-- rETH peg query is copied from https://dune.com/queries/1285810.
 blocks AS (
    SELECT
        time,
        "number" AS block
        FROM ethereum.blocks
        WHERE "number" > 13578840
    ),
 -- BalancesUpdated reports a snapshot from a previous block `block`, so we need to get the time at which that
 -- snapshot block # occurred to report the accurate time.
 balances_updated AS (
    SELECT
        block,
        "totalEth" / "rethSupply" AS eth_reth_peg
    FROM rocketnetwork."RocketNetworkBalances_evt_BalancesUpdated"
        WHERE block > 13578840
    ),

peg AS (
    SELECT
        time,
        eth_reth_peg
    FROM blocks b
    JOIN balances_updated d
    ON b.block = d.block
),

joined AS (
    SELECT
        COALESCE(r.time, s.time, p.time) AS time,
        r.reth_amount,
        r.eth_amount,
        s.steth_amount,
        s.eth_amount AS eth_amount_for_steth,
        p.eth_reth_peg
    FROM reth_trades_eth_amount r
    FULL OUTER JOIN steth_trades_eth_amount s
        ON r.time = s.time
    FULL OUTER JOIN peg p
        ON r.time = p.time
),

back_filled AS (
    SELECT
        MAX(time) AS time,
        SUM(eth_amount) / SUM(reth_amount) AS eth_reth_price,
        SUM(eth_amount_for_steth) / SUM(steth_amount) AS eth_steth_price,
        MAX(eth_reth_peg) AS eth_reth_peg,  -- There is only one non-null peg price per group, so use max to snag it.
        SUM(eth_amount) / SUM(reth_amount) / MAX(eth_reth_peg) AS reth_price_peg_ratio,
        SUM(eth_amount) / SUM(reth_amount) / MAX(eth_reth_peg) AS reth_price_peg_pct
    FROM (
        SELECT
            *,
            COUNT(eth_reth_peg) OVER (ORDER BY time DESC) AS peg_group
        FROM joined
    ) g
    GROUP BY peg_group
    ORDER BY time DESC
)

SELECT
    *,
    (reth_price_peg_ratio - 1) AS reth_peg_pct_divergence,
    (eth_steth_price - 1) AS steth_peg_pct_divergence
FROM back_filled
WHERE reth_price_peg_ratio IS NOT NULL  -- Drop the most recent data until the peg is reported.
