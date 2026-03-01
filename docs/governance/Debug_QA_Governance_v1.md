# ARGOS QUANT
## Debug & QA Governance v1.0 (Codex Workflow)

Date: YYYY-MM-DD
Status: Active

---

# 1. Purpose

This document defines the standardized Debug & QA workflow for Argos Quant.

Goal: accelerate implementation while reducing regressions and implementation errors through cross-validation (human + Codex).

---

# 2. Core Principle

- Humans decide **what** and **why** (specification + constraints).
- Codex implements **how** (code changes + PR).
- Humans validate (diff review + invariants + smoke tests).

This is mandatory for production-bound changes.

---

# 3. Workflow (Spec → Implement → QA)

## Step 1 — Spec Package (Human)
A Spec Package must be produced before asking Codex to implement.

It must include:
- Goal
- Scope/files
- Current vs desired behavior
- Invariants (MUST NOT break)
- Required changes checklist
- Acceptance criteria (observable)
- Testing steps
- Deliverable requirements

## Step 2 — Implementation (Codex)
Codex must:
- implement changes
- create a PR
- provide a clear summary
- provide testing evidence / instructions

## Step 3 — QA Cross-Check (Human)
Before merge:
- review `git diff` carefully
- confirm invariants
- compile + smoke test
- verify outputs (Data Window / webhook payload schema)
- confirm no new hidden complexity

---

# 4. Rules of Discipline

1. **1 PR = 1 change** (small, reversible, auditable).
2. No PR without acceptance criteria.
3. No merge without smoke test.
4. No structural refactors inside feature PRs.
5. Respect Architecture Freeze: structural changes require version bump and docs updates.

---

# 5. Pine-Script Constraints (Project-Specific)

- Do not mutate globals inside functions.
- `reset()` must only reset trade-state (must not erase structural maps).
- Cancel pending limit orders on invalidation/reset (no dangling orders).
- Avoid introducing lookahead/repainting.
- If adding logging, keep schema stable (schema_version).

---

# 6. Standard Spec Template (Copy/Paste)

TITLE: <Short imperative title>

GOAL
- <1–2 lines>

SCOPE / FILES
- <file paths>

CONTEXT
- Current behavior:
- Desired behavior:

CONSTRAINTS / INVARIANTS (MUST NOT BREAK)
- 1)
- 2)
- 3)

REQUIRED CHANGES
- [ ] Change A
- [ ] Change B

ACCEPTANCE CRITERIA
- [ ] Compiles without errors
- [ ] Scenario 1: <given/when/then>
- [ ] Data outputs: <fields present, formats>

TESTING
- Steps:
  1)
  2)

DELIVERABLE
- Open a PR with commits + summary + validation steps
