# SpaceX Falcon 9 First-Stage Landing Prediction (IBM Data Science Capstone)

Run the scripts in order. Each writes a CSV or figure used by the next one.

| # | Script | Output |
|---|--------|--------|
| 1 | 1_data_collection_api.py | dataset_part_1.csv |
| 2 | 2_webscraping.py | spacex_web_scraped.csv |
| 3 | 3_data_wrangling.py | dataset_part_2.csv (adds `Class` label) |
| 4 | 4_eda_sql.py | prints SQL results (SQLite) |
| 5 | 5_eda_dataviz.py | figures/*.png, features.csv |
| 6 | 6_folium_map.py | spacex_map.html |
| 7 | 7_spacex_dash_app.py | Plotly Dash app (http://127.0.0.1:8050) |
| 8 | 8_ml_prediction.py | model accuracies, confusion matrix |

Install: `pip install -r requirements.txt`

Data notes: the SpaceX API and Wikipedia pages change over time, so counts can differ
from the course. Scripts 3-8 fall back to the IBM course CSVs (see `COURSE_URL` constants)
if local files are missing.
