import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def scrap_url():
    url = "https://www.cryptocompare.com/coins/list/all/USD/1"
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }
    
    response = session.get(url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    coin_entries = []
    symbol_candidates= []
    for a in soup.find_all("a", class_="popular-item"):
        href = urljoin("https://www.cryptocompare.com", a.get("href", "").strip())
        name_tag = a.find(class_="coins-name")
        name = name_tag.get_text(strip=True) if name_tag else None
        img = a.find("img")
        tick = img.get("title") if img and img.get("title") else None
        coin_entries.append({"name": name, "href": href, "tick": tick})
        if tick:
            symbol_candidates.append(tick.upper())

    # print("Coin Entries :")
    # print(coin_entries)
    # print("Symbol Candidates :")
    # print(symbol_candidates)

    seen = set()
    symbol_candidates_unique = []
    for symbol in symbol_candidates:
        if symbol and symbol not in seen:
            seen.add(symbol)
            symbol_candidates_unique.append(symbol)

    # print("Symbol Candidates Unique :")
    # print(symbol_candidates_unique)

    raw_infos = {}
    if symbol_candidates_unique:
        resp = requests.get(
            "https://min-api.cryptocompare.com/data/pricemultifull",
            params={"fsyms": ",".join(symbol_candidates_unique), "tsyms": "USD"},
            timeout=15
        )
        raw_infos = resp.json().get("RAW", {})

    # print("Raw Infos :")
    # print(raw_infos)

    timestamp = datetime.now()
    crypto_list = []
    for item in coin_entries:
        symbol = item.get("tick")
        if not symbol:
            continue
        symbol = symbol.upper().strip()
        info = raw_infos.get(symbol, {}).get("USD", {}) or {}
        crypto_list.append({
            "symbol": symbol,
            "name": item.get("name"),
            "price": info.get("PRICE"),
            "volume": info.get("VOLUME24HOURTO") or info.get("TOTALVOLUME24H"),
            "change_24h": info.get("CHANGEPCT24HOUR") or info.get("CHANGE24HOUR"),
            "timestamp": timestamp
        })

    # print("Final Crypto List :")
    # print(crypto_list)
    
    with open("scrapper_sc1.json", "w", encoding="utf-8") as f:
        import json
        json.dump({"coin_entries": coin_entries}, f, ensure_ascii=False, indent=4)
        json.dump({"symbol_candidates": symbol_candidates}, f, ensure_ascii=False, indent=4)
        json.dump({"symbol_candidates_unique": symbol_candidates_unique}, f, ensure_ascii=False, indent=4)
        json.dump({"raw_infos": raw_infos}, f, ensure_ascii=False, indent=4)
        json.dump({"crypto_list": crypto_list}, f, ensure_ascii=False, indent=4)

    return crypto_list

# scrap_url()