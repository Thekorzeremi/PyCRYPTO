import json
import scrapperCryptocompare as sc1
import scrapperCoursCryptomonnaies as sc2
from sqlalchemy.orm import Session
from db import SessionLocal as DBSession
from ingest import ingest_market_data, ingest_news

def run_pipeline(scrapper):
    session = DBSession()
    crypto_data = None
    match scrapper:
        case 1:
            crypto_data1 = sc1.scrap_url()
            crypto_data = crypto_data1
        case 2:
            crypto_data2 = sc2.scrap_url()
            crypto_data = crypto_data2
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
