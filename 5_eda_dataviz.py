"""EDA with visualisation + feature engineering."""
import os, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
COURSE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df = pd.read_csv("dataset_part_2.csv" if os.path.exists("dataset_part_2.csv") else COURSE_URL)
os.makedirs("figures", exist_ok=True)
def save(n): plt.tight_layout(); plt.savefig(f"figures/{n}.png", dpi=130); plt.close()
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=3); save("flight_vs_site")
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect=3); save("payload_vs_site")
sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect=3); save("flight_vs_orbit")
sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df, aspect=3); save("payload_vs_orbit")
df.groupby("Orbit")["Class"].mean().sort_values(ascending=False).plot.bar(); plt.ylabel("Success rate"); save("orbit_success")
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df.groupby("Year")["Class"].mean().plot(marker="o"); plt.ylabel("Success rate"); plt.grid(alpha=.3); save("yearly_trend")
feat = df[["FlightNumber","PayloadMass","Orbit","LaunchSite","Flights","GridFins","Reused","Legs","LandingPad","Block","ReusedCount","Serial"]]
feat = pd.get_dummies(feat, columns=["Orbit","LaunchSite","LandingPad","Serial"]).astype(float)
feat.to_csv("features.csv", index=False); print(feat.shape)
