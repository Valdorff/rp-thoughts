WITH

mainnet AS (
SELECT
  evt_block_time AS time,
  'mainnet' as chain,
  to AS to,
  "from" AS "from",
  evt_tx_hash AS hash,
  IF(to = 0xb867EA3bBC909954d737019FEf5AB25dFDb38CB9, CAST(value as DOUBLE), -1*CAST(value as DOUBLE)) as rplChange
FROM
  rocketpool_ethereum.RocketTokenRPL_evt_Transfer
WHERE to = 0xb867EA3bBC909954d737019FEf5AB25dFDb38CB9  -- IMC multisig
OR "from" = 0xb867EA3bBC909954d737019FEf5AB25dFDb38CB9  -- IMC multisig
),

arbitrum AS (
SELECT
  evt_block_time AS time,
  'arbitrum' as chain,
  to AS to,
  "from" AS "from",
  evt_tx_hash AS hash,
  IF(to = 0xd7102A3744c302f167c53621453516345bC460d7, CAST(value as DOUBLE), -1*CAST(value as DOUBLE)) as rplChange
FROM
  erc20_arbitrum.evt_Transfer
WHERE contract_address = 0xB766039cc6DB368759C1E56B79AFfE831d0Cc507
AND (to = 0xd7102A3744c302f167c53621453516345bC460d7  -- IMC multisig
OR "from" = 0xd7102A3744c302f167c53621453516345bC460d7)  -- IMC multisig
),

data AS (
SELECT * FROM mainnet
UNION ALL
SELECT * FROM arbitrum
)

SELECT
  time,
  chain,
  hash,
  rplChange/1e18 as "RPL Change",
  (SUM(rplChange) over (ORDER BY time ASC))/1e18 AS "Net RPL"
FROM
  data
ORDER BY time desc