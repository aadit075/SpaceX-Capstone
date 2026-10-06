"""Clean data and create the binary landing label `Class`."""
import os, pandas as pd
COURSE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
df = pd.read_csv("dataset_part_1.csv" if os.path.exists("dataset_part_1.csv") else COURSE_URL)
print(df.isnull().sum() / len(df) * 100)
df["PayloadMass"] = df["PayloadMass"].fillna(df["PayloadMass"].mean())
print(df["LaunchSite"].value_counts()); print(df["Orbit"].value_counts())
print(df["Outcome"].value_counts())
bad = {"False Ocean", "False RTLS", "False ASDS", "None ASDS", "None None"}
df["Outcome"] = df["Outcome"].astype(str).str.strip()
df["Class"] = [0 if (o in bad or o == "nan") else 1 for o in df["Outcome"]]
print("Success rate:", df["Class"].mean())
df.to_csv("dataset_part_2.csv", index=False)
