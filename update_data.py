import json
import PyCRYPTO.scrapperCryptocompare as sc1
import PyCRYPTO.scrapperCoursCryptomonnaies as sc2
from sqlalchemy.orm import Session
from db import SessionLocal as DBSession
from ingest import ingest_market_data, ingest_news

def run_pipeline(scrapper):
    session = DBSession()
    crypto_data = None
    match scrapper:
        case "cryptocompare":
            crypto_data1 = sc1.scrap_url()
            crypto_data = crypto_data1
        case "courscryptomonnaies":
            crypto_data2 = sc2.scrap_url()
            crypto_data = crypto_data2
        case _:
            pass
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
