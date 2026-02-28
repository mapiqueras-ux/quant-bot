from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.db import init_db, insert_event

app = FastAPI(title="quant-bot backend", version="0.1.0")


class TradingViewEvent(BaseModel):
    schema_version: str = Field(default="1.0")
    event_id: str
    event_type: str  # e.g. "entry" | "exit" | "signal"
    symbol: str
    timeframe: str | None = None
    ts_utc: str | None = None  # ISO8601 string
    payload: dict = Field(default_factory=dict)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/webhook/tradingview")
def tradingview_webhook(evt: TradingViewEvent):
    insert_event(evt)
    return {"status": "accepted", "event_id": evt.event_id}
