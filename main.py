from fastapi import FastAPI
from sqlalchemy.orm import Session
from db import SessionLocal as DBSession
from models import CryptoAsset, MarketData
from update_data import run_pipeline

app = FastAPI()

@app.post("/scraping/manual")
def manual_scraping():
    run_pipeline()
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

