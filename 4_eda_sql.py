"""EDA with SQL on SQLite."""
import os, sqlite3, pandas as pd
COURSE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv("Spacex.csv" if os.path.exists("Spacex.csv") else COURSE_URL)
con = sqlite3.connect("my_data1.db"); df.to_sql("SPACEXTBL", con, if_exists="replace", index=False)
print(df.columns.tolist())  # check column names match the queries below
Q = {
 "1 Unique launch sites": 'SELECT DISTINCT "Launch_Site" FROM SPACEXTBL',
 "2 Sites starting with CCA": 'SELECT * FROM SPACEXTBL WHERE "Launch_Site" LIKE \'CCA%\' LIMIT 5',
 "3 Total payload NASA (CRS)": 'SELECT SUM("PAYLOAD_MASS__KG_") FROM SPACEXTBL WHERE "Customer"=\'NASA (CRS)\'',
 "4 Avg payload F9 v1.1": 'SELECT AVG("PAYLOAD_MASS__KG_") FROM SPACEXTBL WHERE "Booster_Version" LIKE \'F9 v1.1%\'',
 "5 First ground pad success": 'SELECT MIN("Date") FROM SPACEXTBL WHERE "Landing_Outcome"=\'Success (ground pad)\'',
 "6 Drone ship success, 4000-6000kg": 'SELECT "Booster_Version" FROM SPACEXTBL WHERE "Landing_Outcome"=\'Success (drone ship)\' AND "PAYLOAD_MASS__KG_" BETWEEN 4000 AND 6000',
 "7 Mission outcome counts": 'SELECT "Mission_Outcome", COUNT(*) FROM SPACEXTBL GROUP BY "Mission_Outcome"',
 "8 Boosters with max payload": 'SELECT DISTINCT "Booster_Version" FROM SPACEXTBL WHERE "PAYLOAD_MASS__KG_"=(SELECT MAX("PAYLOAD_MASS__KG_") FROM SPACEXTBL)',
 "9 2015 drone ship failures": 'SELECT "Date","Booster_Version","Launch_Site" FROM SPACEXTBL WHERE "Landing_Outcome"=\'Failure (drone ship)\' AND substr("Date",1,4)=\'2015\'',
 "10 Outcome ranking 2010-06-04..2017-03-20": 'SELECT "Landing_Outcome", COUNT(*) c FROM SPACEXTBL WHERE "Date" BETWEEN \'2010-06-04\' AND \'2017-03-20\' GROUP BY "Landing_Outcome" ORDER BY c DESC',
}
for k, q in Q.items():
    print("\n==", k); print(pd.read_sql(q, con).to_string(index=False))
