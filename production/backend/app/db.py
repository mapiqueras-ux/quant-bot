import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "sqlite" / "quantbot.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
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


def insert_event(evt):
    payload_json = json.dumps(evt.payload, ensure_ascii=False, separators=(",", ":"))

    with get_conn() as conn:
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
