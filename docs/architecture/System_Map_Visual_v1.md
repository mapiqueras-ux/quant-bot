# ARGOS QUANT
## System Master Map v1.0

---

# 1. Purpose

This document provides the unified visual map of Argos Quant.

It connects:

Strategy → Signal Layer → Execution → Broker → Data → Reconciliation → Research → Governance

This is the single high-level reference of the system.

---

# 2. Master Architecture Overview

                          ┌─────────────────────────────┐
                          │        STRATEGY LAYER        │
                          │  TradingView (Cloud)         │
                          │  Pine S1 FSM                 │
                          │  - Sweep / Shift / FVG       │
                          │  - Trap / Risk calc          │
                          │  - Features (Instability)    │
                          └───────────────┬─────────────┘
                                          │
                                          │ (1) ORDER_INTENT (Webhook JSON)
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CONTROL & ROUTING LAYER                            │
│                                                                              │
│  Signal Gateway (FastAPI)                                                    │
│   - Auth                                                                      │
│   - Schema validation                                                         │
│   - Idempotency                                                               │
│   - Intent persistence                                                         │
│                                                                              │
│  Execution Bridge                                                             │
│   - Queue                                                                     │
│   - Account routing                                                            │
│   - Risk pre-checks                                                            │
│   - Retry logic                                                                │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ (2) EXECUTION COMMAND
                                ▼
┌───────────────────────────────┐
│         EXECUTION NODE        │
│  Windows VPS                  │
│  MT5 Terminal(s)              │
│  Expert Advisor               │
│  AutoTrading ON               │
└───────────────┬───────────────┘
                │
                │ (3) Broker Interaction
                ▼
┌───────────────────────────────┐
│           BROKER              │
│  - Fills                      │
│  - Slippage                   │
│  - Commission / Swap          │
│  - Rejections                 │
└───────────────┬───────────────┘
                │
                │ (4) EXECUTION REPORTS
                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                               DATA LAYER                                     │
│                                                                              │
│  PostgreSQL (Source of Truth)                                                │
│   - intents                                                                  │
│   - execution_events                                                          │
│   - reconciliation                                                            │
│                                                                              │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        RESEARCH & MONITORING LAYER                           │
│                                                                              │
│  Edge Stability Monitor (ESM)                                                │
│   - Baseline vs Live                                                          │
│   - Slippage-adjusted expectancy                                              │
│   - Regime segmentation                                                       │
│                                                                              │
│  Research Lab (iMac)                                                         │
│   - Ablation tests                                                            │
│   - Walk-forward                                                              │
│   - Monte Carlo                                                               │
│   - Strategy evolution                                                        │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              GOVERNANCE LAYER                                │
│                                                                              │
│  Research → Incubator → Production                                           │
│  Version control (Git tags)                                                  │
│  Promotion criteria                                                           │
│  Capital scaling rules                                                        │
│  Emergency shutdown protocol                                                  │
└──────────────────────────────────────────────────────────────────────────────┘

# 3. Layer Responsibilities

** Strategy Layer
Generates edge and feature context.
Does NOT execute trades.

** Control Layer
Validates, routes, protects, and logs intentions.

** Execution Layer
Places real trades through MT5 and broker.

** Data Layer
Maintains immutable execution truth.

** Research Layer
Evaluates edge stability and execution quality.

** Governance Layer
Controls promotion, rollback, and capital scaling.

# 4. Physical Deployment Summary

TradingView → Cloud
Signal Gateway + DB → Railway / VPS
Execution Node → Windows VPS
Research → Local iMac

Local machines are NEVER execution-critical.

# 5. Data Authority Principle

Broker execution data is the ultimate source of truth.

Strategy intent is immutable.

Reconciliation connects both.

# 6. Strategic Separation

Edge generation and execution are decoupled.

This allows:

- Multi-broker routing
- Prop-firm scaling
- Portfolio expansion
- Execution benchmarking
- Institutional discipline

# 7. System Identity

Argos Quant is not a script.

It is a modular trading infrastructure composed of:

* Signal intelligence
* Execution control
* Data governance
* Statistical validation
* Institutional promotion framework
