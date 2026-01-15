import json
import scrapper
from sqlalchemy.orm import Session
from db import SessionLocal as DBSession
from ingest import ingest_market_data, ingest_news

def run_pipeline():
    session = DBSession()
    crypto_data = scrapper.scrap_url()
    print(crypto_data)
    try:
        if crypto_data:
            ingest_market_data(session, crypto_data)
        else:
            with open("scrapper_json.json", "r") as f:
                data = json.load(f)
                if "crypto" in data:
                    ingest_market_data(session, data["crypto"])
                if "news" in data:
                    ingest_news(session, data["news"])
    finally:
        session.close()

run_pipeline()
