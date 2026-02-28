import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import psycopg


BASE_DIR = Path(__file__).resolve().parents[3]
SQLITE_PATH = BASE_DIR / "data" / "sqlite" / "quantbot.db"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


def _is_postgres(url: str) -> bool:
    if not url:
        return False
    scheme = urlparse(url).scheme.lower()
    return scheme in {"postgres", "postgresql"}


def init_db() -> None:
    if _is_postgres(DATABASE_URL):
        _init_postgres()
    else:
        _init_sqlite()


def insert_event(evt) -> None:
    if _is_postgres(DATABASE_URL):
        _insert_postgres(evt)
    else:
        _insert_sqlite(evt)


# -----------------------
# SQLite
# -----------------------
def _sqlite_conn():
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(SQLITE_PATH)


def _init_sqlite() -> None:
    with _sqlite_conn() as conn:
        conn.execute(
            """
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
            )
            """
        )


def _insert_sqlite(evt) -> None:
    payload_json = json.dumps(evt.payload, ensure_ascii=False, separators=(",", ":"))
    with _sqlite_conn() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO trade_events
            (event_id, schema_version, source, strategy_id, event_type, symbol, timeframe, ts_utc, payload_json, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evt.event_id,
                getattr(evt, "schema_version", "1.0"),
                getattr(evt, "source", "tradingview"),
                getattr(evt, "strategy_id", None),
                evt.event_type,
                evt.symbol,
                evt.timeframe,
                evt.ts_utc,
                payload_json,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


# -----------------------
# Postgres (Railway)
# -----------------------
def _pg_conn():
    # Railway provides DATABASE_URL
    return psycopg.connect(DATABASE_URL)


def _init_postgres() -> None:
    with _pg_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trade_events (
                id BIGSERIAL PRIMARY KEY,
                event_id TEXT UNIQUE,
                schema_version TEXT,
                source TEXT,
                strategy_id TEXT,
                event_type TEXT,
                symbol TEXT,
                timeframe TEXT,
                ts_utc TEXT,
                payload_json JSONB,
                received_at TIMESTAMPTZ
            );
            """
        )


def _insert_postgres(evt) -> None:
    payload_json = evt.payload  # keep as native dict -> JSONB
    with _pg_conn() as conn:
        conn.execute(
            """
            INSERT INTO trade_events
            (event_id, schema_version, source, strategy_id, event_type, symbol, timeframe, ts_utc, payload_json, received_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (event_id) DO NOTHING;
            """,
            (
                evt.event_id,
                getattr(evt, "schema_version", "1.0"),
                getattr(evt, "source", "tradingview"),
                getattr(evt, "strategy_id", None),
                evt.event_type,
                evt.symbol,
                evt.timeframe,
                evt.ts_utc,
                payload_json,
                datetime.now(timezone.utc),
            ),
        )
