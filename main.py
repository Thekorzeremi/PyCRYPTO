from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import SessionLocal as DBSession
from models import CryptoAsset
from scheduler import start_scheduler, shutdown_scheduler
from update_data import run_pipeline_multithread
from datetime import datetime, timedelta, timezone

@asynccontextmanager
async def lifespan(_app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)

@app.post("/scraping/manual")
def manual_scraping():
    run_pipeline_multithread()
    return {"status": "ok", "message": "Scraping manuel exécuté en parallèle"}

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

@app.get("/crypto/{symbol}/stats")
def crypto_stats(symbol: str, last_hours: int = 24):
    session = DBSession()
    try:
        crypto = session.query(CryptoAsset).filter_by(symbol=symbol).first()
        if not crypto:
            raise HTTPException(status_code=404, detail="CryptoAsset non trouvé")

        cutoff = datetime.now(timezone.utc) - timedelta(hours=last_hours)
        data_points = [md for md in crypto.market_data if md.timestamp >= cutoff]

        if not data_points:
            return {"symbol": symbol, "message": f"Aucune donnée dans les {last_hours} dernières heures"}

        prices = [md.price for md in data_points if md.price is not None]
        volumes = [md.volume for md in data_points if md.volume is not None]
        changes = [md.change_24h for md in data_points if md.change_24h is not None]

        stats = {
            "symbol": symbol,
            "count": len(data_points),
            "avg_price": sum(prices)/len(prices) if prices else None,
            "avg_volume": sum(volumes)/len(volumes) if volumes else None,
            "avg_change_24h": sum(changes)/len(changes) if changes else None,
            "min_price": min(prices) if prices else None,
            "max_price": max(prices) if prices else None,
            "price_variation": prices[-1]-prices[0] if len(prices)>=2 else None
        }
        return stats
    finally:
        session.close()
