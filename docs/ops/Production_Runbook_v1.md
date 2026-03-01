# ARGOS QUANT
## Production Runbook v1.0

---

# 1. Purpose

This document defines the operational procedure for running Argos Quant in production mode.

It ensures:

- Signals are active
- Execution pipeline is functional
- Data collection is intact
- Reconciliation is consistent
- Risk exposure is controlled

This is the authoritative checklist before capital is exposed.

---

# 2. System Overview

Production stack:

TradingView → Signal Gateway → Execution Bridge → MT5 → Broker → Reconciliation → Monitoring

Execution must NEVER depend on local machines.

---

# 3. Pre-Production Checklist

## 3.1 TradingView

- Script version tagged (bot_version updated)
- Chart saved
- Alerts created
- Alerts set to:
  - Webhook URL correct
  - API key valid
  - No expiration (or far future)
- Alert test triggered successfully
- Confirm alert still triggers after:
  - Closing browser
  - Logging out
  - Rebooting local machine

---

## 3.2 Backend (Railway/VPS)

- Server status: running
- Environment variables set:
  - API_KEY
  - DATABASE_URL
- DB connection verified
- Ingest endpoint responding (HTTP 200)
- Duplicate event protection active

---

## 3.3 Execution Bridge

- Worker process running
- Queue consumption verified
- Retry logic enabled
- No stuck pending jobs

---

## 3.4 MT5 Node

- VPS online
- MT5 terminal running
- EA loaded
- AutoTrading enabled
- Broker connected
- Correct account logged in
- Symbol names aligned with TradingView mapping
- Trade_id propagation confirmed (if supported)

---

## 3.5 Reconciliation

- Execution events arriving in DB
- Intent ↔ Execution matching successful
- Slippage calculated correctly
- No unmatched trades older than threshold

---

# 4. Go-Live Procedure

1. Deploy new bot_version
2. Create fresh TradingView alerts
3. Confirm webhook test
4. Verify backend ingest
5. Place small test trade (micro lot)
6. Verify:
   - Intent recorded
   - Order placed in MT5
   - Fill recorded
   - Reconciliation matched
7. Confirm PnL consistency

Only then increase exposure.

---

# 5. Live Monitoring

Monitor daily:

- Server uptime
- Alert trigger count
- Execution success rate
- Slippage distribution
- Unmatched intents
- MT5 connection status

Weekly:

- Execution quality metrics
- Cost per trade
- Cost per R
- Divergence flags

---

# 6. Failure Protocol

## Case 1 – No signals triggered

- Check TradingView alerts
- Check expiration
- Recreate alert

## Case 2 – Signals but no execution

- Check Execution Bridge
- Check MT5 AutoTrading
- Check symbol mapping

## Case 3 – Execution but no reconciliation

- Check collector
- Check DB connection
- Check trade_id propagation

## Case 4 – Duplicate trades

- Verify idempotency logic
- Check event_id uniqueness

---

# 7. Capital Scaling Rules

Capital may be increased only if:

- Execution-adjusted expectancy > 0
- Slippage within tolerance
- No structural divergence
- ESM status green or stable yellow

---

# 8. Governance

Every production version must:

- Have version tag in Git
- Have bot_version embedded in payload
- Be documented in changelog
- Have rollback version available

---

# 9. Emergency Shutdown

Immediate shutdown triggers:

- Reconciliation failure
- Unexpected broker behavior
- Massive slippage anomaly
- Backend unavailable
- Execution loop error

Procedure:

1. Disable MT5 AutoTrading
2. Cancel pending orders
3. Close open positions if required
4. Disable TradingView alerts
5. Investigate

---

# 10. Long-Term Discipline

Production mode is a controlled environment.

Research modifications must NEVER be deployed directly.

Promotion path:

Research → Incubator → Controlled Live → Full Production
