from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import CryptoAsset, MarketData, News

def ingest_market_data(session: Session, json_data: list):
    for crypto in json_data:
        asset = session.query(CryptoAsset).filter_by(symbol=crypto["symbol"]).first()
        if not asset:
            asset = CryptoAsset(symbol=crypto["symbol"], name=crypto["name"])
            session.add(asset)
            session.flush()

        md = MarketData(
            price=crypto["price"],
            volume=crypto["volume"],
            change_24h=crypto["change_24h"],
            timestamp=datetime.fromisoformat(crypto["timestamp"].replace("Z", "+00:00")),
            asset=asset
        )
        session.add(md)

    session.commit()

def ingest_news(session: Session, news_json: list):
    for article in news_json:
        # Vérifier doublon
        exists = session.query(News).filter_by(title=article["title"], source_name=article["source_name"]).first()
        if exists:
            continue
        n = News(
            title=article["title"],
            content=article["content"],
            published_at=datetime.fromisoformat(article["published_at"].replace("Z", "+00:00")),
            source_name=article["source_name"]
        )
        session.add(n)
    session.commit()
