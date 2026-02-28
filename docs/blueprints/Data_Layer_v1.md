# Data Layer v1 (trade_events)

## Purpose
Persist all inbound trading events (initially from TradingView webhooks) in a durable, queryable format to enable:
- Debug & audit trail
- Walk-forward evaluation
- Monte Carlo on R-multiples / outcomes
- Edge Stability Monitor (baseline vs live)
- Future ML scoring datasets

## Storage
- **SQLite** local DB (Phase 1): `data/sqlite/quantbot.db`
- Table: `trade_events`
- Data folder is local-only; DB files are ignored by git.

## Idempotency
- `event_id` is **UNIQUE**
- Inserts use **INSERT OR IGNORE**
- Replayed webhooks (duplicates) do not create duplicated rows.

## Security (Webhook)
- Endpoint requires header: `X-API-Key: <token>`
- Server must have env var `API_KEY` set, otherwise startup is considered misconfigured.

## Table schema (SQLite)

```sql
CREATE TABLE IF NOT EXISTS trade_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT UNIQUE,
  schema_version TEXT,
  source TEXT,
  strategy_id TEXT,
  event_type TEXT,
  symbol TEXT,
  timeframe TEXT,
  ts_utc TEXT,
  payload_json TEXT,
  received_at TEXT
);

Column semantics

id: local autoincrement primary key

event_id: globally unique identifier for the event (idempotency key)

schema_version: schema version of the event payload (default "1.0")

source: event source (default "tradingview")

strategy_id: strategy identifier (e.g., "S1")

event_type: event type (e.g., signal, entry, exit)

symbol: instrument (e.g., EURUSD, XAUUSD)

timeframe: optional timeframe (e.g., M5, M15)

ts_utc: optional event timestamp in UTC (ISO8601)

payload_json: JSON string with event-specific fields (compact JSON)

received_at: server receive timestamp in UTC (ISO8601)

Inbound webhook contract (minimum)
Endpoint

POST /webhook/tradingview

Header: X-API-Key: <API_KEY>

Minimal JSON body
{
  "schema_version": "1.0",
  "source": "tradingview",
  "strategy_id": "S1",
  "event_id": "unique-id-here",
  "event_type": "signal",
  "symbol": "EURUSD",
  "timeframe": "M5",
  "ts_utc": "2026-02-28T12:00:00Z",
  "payload": {
    "note": "any extra fields here"
  }
}
Notes / Next steps

Add event_hash (optional) for integrity checks.

Consider normalizing key fields into separate tables once volume grows.

Phase 2: migrate storage to PostgreSQL (Railway managed Postgres) keeping idempotency on event_id.
