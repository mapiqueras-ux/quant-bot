import os
import secrets
from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.db import init_db, insert_event

app = FastAPI(title="quant-bot backend", version="0.1.0")

API_KEY = os.getenv("API_KEY")


class TradingViewEvent(BaseModel):
    schema_version: str = Field(default="1.0")
    event_id: str
    event_type: str
    symbol: str
    timeframe: str | None = None
    ts_utc: str | None = None
    payload: dict = Field(default_factory=dict)


@app.on_event("startup")
def startup_event():
    init_db()


def require_api_key(x_api_key: str | None) -> None:
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfigured: API_KEY not set",
        )
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )


@app.get("/health")
def health():
    return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/webhook/tradingview")
def tradingview_webhook(
    evt: TradingViewEvent,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    insert_event(evt)
    return {"status": "accepted", "event_id": evt.event_id}
