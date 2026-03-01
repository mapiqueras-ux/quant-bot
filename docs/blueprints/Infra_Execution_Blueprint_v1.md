# ARGOS QUANT
## Infrastructure & Execution Blueprint v1.0

---

# 1. Purpose

This document defines the scalable execution architecture of Argos Quant:

TradingView (signal generation) → Backend (control layer) → MT5 (execution) → Broker → Reconciliation → Research & Monitoring.

The architecture separates:

- Strategy logic (edge generation)
- Execution (broker interaction)
- Data truth (real fills)
- Research & stability monitoring

---

# 2. Architectural Principle

TradingView does NOT execute trades.

It only generates **Order Intent Events**.

Execution is performed externally via MT5 + Broker.

This ensures:
- Broker independence
- Prop-firm scalability
- Multi-account routing
- Execution auditability
- Slippage measurement
- Reconciliation capability

---

# 3. Logical Architecture

TradingView (Cloud)
    ↓ (A) Webhook JSON – ORDER_INTENT
Signal Gateway (FastAPI – Cloud)
    ↓ (B) Queue / Dispatch
Execution Bridge (Worker)
    ↓ (C) Command to MT5
MT5 Terminal + EA
    ↓ (D) Execution Reports
Broker
    ↓
Execution Collector
    ↓
PostgreSQL (Source of Truth)
    ↓
Research / ESM / Monitoring

---

# 4. Flow Definitions

## Flow A – Intent (Signal Layer)

Source: TradingView
Destination: Backend Ingest API

Contains:
- event_id (UUID)
- trade_id (UUID)
- bot_version
- account_route
- symbol
- side
- order_type
- entry_price
- sl
- tp
- expiry
- features (JSON)
- timestamp_tv

Purpose:
- Record strategy intention
- Preserve feature context
- Enable reproducibility
- Enable audit

---

## Flow B – Execution Truth

Source: MT5 / Broker
Destination: Execution Collector

Contains:
- broker_ticket_id
- position_id
- symbol
- side
- fill_price
- fill_qty
- commission
- swap
- status
- timestamp_broker

Purpose:
- Real execution data
- Slippage calculation
- Cost measurement
- Ground truth PnL

---

## Flow C – Reconciliation

Performed inside backend layer.

Matches:
Intent.trade_id ↔ Execution.ticket/position

Calculates:
- Slippage
- Latency
- Fill ratio
- Execution divergence
- Net cost
- Execution outcome

Produces:
Reconciled trade record.

---

# 5. Physical Deployment Model

TradingView:
- Cloud hosted
- Always running if alerts active

Core Server (Railway/VPS):
- FastAPI Ingest
- Execution Bridge Worker
- PostgreSQL database

Execution Nodes:
- Windows VPS instances
- MT5 Terminal(s)
- Expert Advisor (EA)
- Execution Collector agent

Research Node:
- Local iMac
- Jupyter / Python analysis
- Edge Stability Monitor

---

# 6. Scaling Model

Scalability is achieved via:

- account_route routing
- Multiple MT5 instances
- Multi-broker abstraction
- Stateless signal generation
- Centralized data layer

One signal → N accounts possible.

---

# 7. Operational Assumptions

- Idempotency required (no duplicate orders)
- MT5 EA must propagate trade_id when possible
- Execution truth is always authoritative
- Strategy layer never modifies historical truth

---

# 8. Future Extensions

- Risk engine pre-execution
- Multi-strategy portfolio router
- Execution quality scoring
- Slippage anomaly detection
- Broker performance comparison module
