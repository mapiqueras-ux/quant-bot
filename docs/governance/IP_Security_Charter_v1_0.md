# ARGOS QUANT
## IP & Security Charter v1.0

Date: YYYY-MM-DD
Status: Active

---

# 1. Purpose

This document defines the intellectual property protection and security principles governing Argos Quant.

Argos Quant is considered proprietary infrastructure.

All components are protected under internal IP governance.

---

# 2. Intellectual Property Scope

Protected assets include:

- Strategy logic (S1 FSM structure)
- Signal feature engineering
- Instability scoring framework
- Execution routing logic
- Reconciliation logic
- Edge Stability Monitor methodology
- Data architecture
- Governance framework
- Documentation

No component may be externally shared without explicit authorization.

---

# 3. Code Protection Principles

- No strategy logic published publicly.
- No Pine scripts exposed.
- No payload schema exposed externally.
- No execution routing disclosed.
- Repository access restricted.
- Production credentials never stored in repo.

---

# 4. Secrets Management

The following must NEVER be committed:

- API keys
- Broker credentials
- Database URLs
- VPS credentials
- MT5 account numbers
- Private endpoints

Use:

- Environment variables
- .env files excluded via .gitignore
- Cloud secret managers where applicable

---

# 5. Access Control

Access levels:

Research:
- Strategy development
- No production credentials

Execution:
- Limited access to execution nodes

Admin:
- Infrastructure access
- Deployment control

No shared credentials.

---

# 6. Production Security Requirements

- HTTPS only
- API authentication mandatory
- Idempotent order handling
- Execution confirmation required
- Emergency shutdown procedure documented

---

# 7. Data Integrity

- Execution truth is immutable
- Intent records immutable
- Reconciliation logs preserved
- No retroactive modification of trade history

---

# 8. Incident Protocol

If compromise suspected:

1. Disable MT5 AutoTrading
2. Rotate API keys
3. Rotate DB credentials
4. Revoke cloud tokens
5. Review access logs
6. Audit recent trades

---

# 9. Strategic Position

Argos Quant is not a public project.
It is a proprietary quantitative infrastructure.

Confidentiality is mandatory.

---

# 10. Amendment Rule

Any structural change affecting security or IP must require:

- Version update
- Written review
- Governance approval
