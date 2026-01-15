from sqlalchemy.orm import Session
from db import engine
from models import CryptoAsset, MarketData, News, ExchangeSource, NewsSource
from datetime import datetime, timezone

session = Session(bind=engine)

# Créer un asset
btc = CryptoAsset(symbol="BTC", name="Bitcoin")
session.add(btc)
session.commit()

# Ajouter un MarketData
data = MarketData(price=30000, volume=1000, change_24h=5, asset=btc)
session.add(data)
session.commit()

source = ExchangeSource(name="Binance", url="https://api.binance.com")
session.add(source)
session.commit()

# Vérifier dans la DB
for asset in session.query(CryptoAsset).all():
    print(asset.symbol, asset.name)

session.close()
