# ARGOS QUANT
## Data & Reconciliation Blueprint v1.0

---

# 1. Purpose

Define the data model and reconciliation logic between:

- Strategy Intent
- Broker Execution Truth

This layer guarantees:

- Auditability
- Slippage tracking
- Cost transparency
- Edge stability integrity
- Institutional-grade data traceability

---

# 2. Data Model

## Table: intents

Primary Key: event_id

Fields:
- event_id
- trade_id
- bot_version
- account_route
- symbol
- side
- order_type
- entry_price
- sl
- tp
- expiry_ts
- features_json
- timestamp_tv

---

## Table: execution_events

Primary Key: exec_event_id

Fields:
- broker_ticket_id
- position_id
- trade_id (if propagated)
- symbol
- side
- fill_price
- fill_qty
- commission
- swap
- status
- timestamp_broker

---

## Table: reconciliation

Primary Key: trade_id

Fields:
- matched (boolean)
- match_method
- slippage
- latency_ms
- total_cost
- outcome_exec
- partial_fill_flag
- divergence_flag
- notes

---

# 3. Reconciliation Logic

Priority match order:

1. Direct trade_id propagation
2. Ticket mapping from EA
3. Heuristic match:
   - symbol
   - side
   - price proximity
   - time window

After match:

Compute:

slippage = fill_price - intent_price
latency = timestamp_broker - timestamp_tv
net_cost = commission + swap

---

# 4. Integrity Rules

- Execution truth overrides intent
- Intent cannot be modified post factum
- All mismatches logged
- Late fills after cancel flagged
- Partial fills tracked explicitly

---

# 5. Metrics Derived

Execution Quality KPIs:

- Average slippage
- Slippage distribution
- Fill ratio
- Cancel ratio
- Latency distribution
- Cost per trade
- Cost per R
- Execution-adjusted expectancy

---

# 6. Research Interface

Research layer consumes:

- Reconciled trades
- Execution-adjusted PnL
- Slippage-aware expectancy
- Regime segmentation

This ensures the Edge Stability Monitor uses real execution data when in production mode.

---

# 7. Production Governance

Promotion criteria from Research → Production must include:

- Slippage tolerance validated
- Execution stability verified
- No systematic divergence
- Cost-adjusted edge > 0

---

# 8. Long-Term Evolution

- Broker performance benchmarking
- Smart routing
- Adaptive slippage model
- Latency-aware strategy adaptation
