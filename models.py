from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from db import Base


class DataSourceMixin:
    def fetch_data(self):
        raise NotImplementedError("fetch_data must be implemented")

    def parse_data(self, raw_data):
        raise NotImplementedError("parse_data must be implemented")

class ExchangeSource(Base, DataSourceMixin):
    __tablename__ = "exchange_sources"
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)

    def fetch_data(self):
        print("Exchange fetch logic here")

    def parse_data(self, raw_data):
        print("Exchange parse logic here")

class NewsSource(Base, DataSourceMixin):
    __tablename__ = "news_sources"
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)

    def fetch_data(self):
        print("News fetch logic here")

    def parse_data(self, raw_data):
        print("News parse logic here")

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)

    market_data = relationship("MarketData", back_populates="asset")

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    volume = Column(Float)
    change_24h = Column(Float)
    timestamp = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))
    asset_id = Column(Integer, ForeignKey("crypto_assets.id"))
    asset = relationship("CryptoAsset", back_populates="market_data")

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published_at = Column(DateTime)

    source_name = Column(String)

