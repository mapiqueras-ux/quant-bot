import sqlite3
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
                event_type TEXT,
                symbol TEXT,
                timeframe TEXT,
                ts_utc TEXT,
                payload TEXT,
                received_at TEXT
            )
            """
        )


def insert_event(evt):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO trade_events
            (event_id, event_type, symbol, timeframe, ts_utc, payload, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evt.event_id,
                evt.event_type,
                evt.symbol,
                evt.timeframe,
                evt.ts_utc,
                str(evt.payload),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
