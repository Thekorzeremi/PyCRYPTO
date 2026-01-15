import requests
import json
import re
from bs4 import BeautifulSoup

def scrap_url():
    url = "https://www.courscryptomonnaies.com/"
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

    push_pattern = re.compile(r'self\.__next_f\.push\(\[1,.*?\]\)\s*', re.S)

    extracted_push_blocks = []

    for script_tag in soup.find_all("script"):
        for match in push_pattern.finditer(script_tag.get_text()):
            extracted_push_blocks.append(match.group(0).strip())

    crypto_push_blocks = []
    for block in extracted_push_blocks:
        if "crypto-logos" in block:
            if "overflow-hidden border-y border-slate-200 bg-white" not in block:
                crypto_push_blocks.append(block)

    crypto_list = []

    for block in crypto_push_blocks:

        def unescape_js(js_string):
            try:
                decoded = bytes(js_string, "utf-8").decode("unicode_escape")
            except Exception:
                decoded = js_string
            try:
                decoded = decoded.encode("latin-1").decode("utf-8")
            except Exception:
                pass
            return decoded

        cleaned_block = unescape_js(block)

        logo_match = re.search(r'"src"\s*:\s*"([^"]+)"|src="([^"]+)"', cleaned_block)
        logo_url = logo_match.group(1) or logo_match.group(2) if logo_match else None

        alt_match = re.search(r'"alt"\s*:\s*"([^"]+)"|alt="([^"]+)"', cleaned_block)
        alt_text = alt_match.group(1) or alt_match.group(2) if alt_match else None

        price_match = re.search(r'([\d\s\u00A0\u202F.,]+)€', cleaned_block)
        price_eur = price_match.group(1).strip() if price_match else None

        variation_match = re.search(r'([+-]?\d+[.,]?\d*)%', cleaned_block)
        variation_pct = variation_match.group(1) if variation_match else None

        crypto_list.append({
            "name": alt_text,
            "symbol": logo_url,
            "price_eur": price_eur,
            "variation_pct": variation_pct
        })

    with open("coins_only.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(crypto_list, ensure_ascii=False, indent=4))

scrap_url()
