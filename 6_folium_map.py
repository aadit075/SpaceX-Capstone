"""Interactive launch-site map with Folium."""
import os, math, folium, pandas as pd
from folium.plugins import MarkerCluster, MousePosition
COURSE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
df = pd.read_csv("spacex_launch_geo.csv" if os.path.exists("spacex_launch_geo.csv") else COURSE_URL)
sites = df.groupby("Launch Site")[["Lat", "Long"]].first().reset_index()
m = folium.Map(location=[29.56, -95.09], zoom_start=5)
folium.Circle([29.5599, -95.0830], radius=1000, color="#d35400", fill=True).add_child(folium.Popup("NASA JSC")).add_to(m)
for _, r in sites.iterrows():
    folium.Circle([r.Lat, r.Long], radius=1000, color="#1F6FEB", fill=True).add_to(m)
    folium.Marker([r.Lat, r.Long], icon=folium.DivIcon(html=f'<div style="font-size:12px;color:#1F6FEB"><b>{r["Launch Site"]}</b></div>')).add_to(m)
cluster = MarkerCluster().add_to(m)
for _, r in df.iterrows():
    folium.Marker([r.Lat, r.Long], icon=folium.Icon(color="white", icon_color="green" if r["class"] == 1 else "red")).add_to(cluster)
MousePosition().add_to(m)
def hav(a, b, c, d):
    R = 6371; p1, p2 = math.radians(a), math.radians(c); dl = math.radians(d - b); dp = p2 - p1
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))
# proximity: pick coordinates by hovering with MousePosition, then edit below
site = (28.563197, -80.576820)
for name, pt in {"Coastline": (28.56367, -80.57163), "Railway": (28.57206, -80.58528),
                 "Highway": (28.56287, -80.57083), "City (Melbourne)": (28.10473, -80.64531)}.items():
    d = hav(*site, *pt)
    folium.PolyLine([site, pt], weight=2).add_to(m)
    folium.Marker(pt, icon=folium.DivIcon(html=f'<div style="font-size:11px">{name}: {d:.2f} km</div>')).add_to(m)
m.save("spacex_map.html"); print("saved spacex_map.html")
