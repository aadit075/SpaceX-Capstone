"""Scrape Falcon 9 launch records from Wikipedia."""
import requests, pandas as pd
from bs4 import BeautifulSoup
URL = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
soup = BeautifulSoup(requests.get(URL, headers={"User-Agent": "capstone-project/1.0"}, timeout=30).text, "html.parser")
tables = soup.find_all("table", "wikitable plainrowheaders collapsible")
cols = ["Flight No.", "Date and time (UTC)", "Version, Booster", "Launch site", "Payload",
        "Payload mass", "Orbit", "Customer", "Launch outcome", "Booster landing"]
data = {c: [] for c in cols}
for t in tables:
    for row in t.find_all("tr")[1:]:
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
        if len(cells) >= len(cols) - 1 and cells[0].isdigit():
            cells = (cells + [""] * len(cols))[:len(cols)]
            for c, v in zip(cols, cells):
                data[c].append(v)
df = pd.DataFrame(data)
df.to_csv("spacex_web_scraped.csv", index=False)
print(df.shape); print(df.head())
