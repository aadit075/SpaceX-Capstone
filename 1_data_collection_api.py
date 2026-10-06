"""Collect Falcon 9 launch data from the SpaceX REST API (v4)."""
import requests, pandas as pd
BASE = "https://api.spacexdata.com/v4"
launches = requests.get(f"{BASE}/launches/past", timeout=30).json()

def lookup(endpoint, ident, cache={}):
    key = (endpoint, ident)
    if key not in cache:
        cache[key] = requests.get(f"{BASE}/{endpoint}/{ident}", timeout=30).json()
    return cache[key]

rows = []
for l in launches:
    if len(l["cores"]) != 1 or len(l["payloads"]) != 1:  # keep single-core, single-payload
        continue
    if not l["cores"][0]["core"]:
        continue
    rocket = lookup("rockets", l["rocket"])
    if rocket["name"] != "Falcon 9":
        continue
    pad = lookup("launchpads", l["launchpad"])
    pay = lookup("payloads", l["payloads"][0])
    core = lookup("cores", l["cores"][0]["core"])
    c = l["cores"][0]
    rows.append({
        "FlightNumber": l["flight_number"], "Date": l["date_utc"][:10],
        "BoosterVersion": rocket["name"], "PayloadMass": pay["mass_kg"], "Orbit": pay["orbit"],
        "LaunchSite": pad["name"], "Outcome": None if c["landing_success"] is None else
            ("True " if c["landing_success"] else "False ") + str(c["landing_type"]),
        "Flights": c["flight"], "GridFins": c["gridfins"], "Reused": c["reused"], "Legs": c["legs"],
        "LandingPad": c["landpad"], "Block": core["block"], "ReusedCount": core["reuse_count"],
        "Serial": core["serial"], "Longitude": pad["longitude"], "Latitude": pad["latitude"]})

df = pd.DataFrame(rows).sort_values("FlightNumber")
df.to_csv("dataset_part_1.csv", index=False)
print(df.shape); print(df.head())
