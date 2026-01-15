from fastapi import FastAPI
from sqlalchemy.orm import Session
from db import SessionLocal as DBSession
from models import CryptoAsset, MarketData
from update_data import run_pipeline
from contextlib import asynccontextmanager
from scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup : démarrage du scheduler
    start_scheduler()
    yield  # application tourne
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)

@app.post("/scraping/manual/{scrapper}")
def manual_scraping(scrapper: int):
    run_pipeline(scrapper)
    return {"status": "ok"}

@app.get("/crypto/{symbol}")
def get_crypto(symbol: str):
    session = DBSession()
    crypto = session.query(CryptoAsset).filter_by(symbol=symbol).first()
    data = [
        {"price": md.price, "volume": md.volume, "change_24h": md.change_24h, "timestamp": md.timestamp.isoformat()}
        for md in crypto.market_data
    ] if crypto else []
    session.close()
    return {"symbol": symbol, "data": data}

