"""Plotly Dash dashboard: success pie + payload vs outcome scatter."""
import os, pandas as pd, plotly.express as px
from dash import Dash, html, dcc, Input, Output
COURSE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
df = pd.read_csv("spacex_launch_dash.csv" if os.path.exists("spacex_launch_dash.csv") else COURSE_URL)
lo, hi = df["Payload Mass (kg)"].min(), df["Payload Mass (kg)"].max()
app = Dash(__name__)
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(id="site", value="ALL", clearable=False,
        options=[{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in df["Launch Site"].unique()]),
    dcc.Graph(id="pie"),
    html.P("Payload range (kg):"),
    dcc.RangeSlider(id="pay", min=0, max=10000, step=1000, value=[lo, hi], marks={i: str(i) for i in range(0, 10001, 2500)}),
    dcc.Graph(id="scatter")])
@app.callback(Output("pie", "figure"), Input("site", "value"))
def pie(site):
    if site == "ALL":
        return px.pie(df[df["class"] == 1], names="Launch Site", title="Total successful launches by site")
    d = df[df["Launch Site"] == site]["class"].value_counts().rename({1: "Success", 0: "Failure"}).reset_index()
    d.columns = ["Outcome", "Count"]
    return px.pie(d, names="Outcome", values="Count", title=f"Success vs failure: {site}")
@app.callback(Output("scatter", "figure"), [Input("site", "value"), Input("pay", "value")])
def scat(site, pay):
    d = df[df["Payload Mass (kg)"].between(*pay)]
    if site != "ALL": d = d[d["Launch Site"] == site]
    return px.scatter(d, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Payload vs launch outcome")
if __name__ == "__main__":
    app.run(debug=True)
