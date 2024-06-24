import math
import webbrowser

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc
from dash.exceptions import PreventUpdate
from plotly.express.colors import sample_colorscale

df = pd.read_csv("data/baraky.csv")

# Filter data
df = df[df["Stavba"] != "Dřevostavba"]
df = df.sort_values(by="state_score")

color_range = np.linspace(0, 1, len(df["state_score"].unique()))
colors = sample_colorscale("jet", color_range)

fig = go.Figure()

# Add a scatter trace for each unique state_score
for score, color in zip(df["state_score"].unique(), colors):
    if math.isnan(score):
        filtered_df = df[df["state_score"].isna()]
    else:
        filtered_df = df[df["state_score"] == score]
    fig.add_trace(go.Scatter(
        x=filtered_df["price"],
        y=filtered_df["prague_trip_min"],
        mode="markers",
        marker=dict(size=10, color=color),
        name=f"State Score {str(score)}",
        customdata=filtered_df[["Voda", "Odpad", "link", "Stav objektu"]],
        hovertemplate='<br>Price: %{x}<br>Prague Trip Min: %{y}<br>Voda: %{customdata[0]}<br>Odpad: %{customdata[1]}<br>Link: <a href="%{customdata[2]}">%{customdata[2]}</a><br>Stav: %{customdata[3]}<extra></extra>'
    ))

fig.update_layout(
    width=900,
    height=650,
    margin={"l": 10, "b": 10, "t": 20, "r": 10}
)
app = Dash(__name__)
app.layout = dcc.Graph(
            id="graph-id",
            figure=fig,
            style={"width": "100%", "display": "inline-block", "height": "1000px"}
        )


@app.callback(Output("graph-id", "figure"), [Input("graph-id", "clickData")])
def open_url(clickData):
    if clickData != None:
        url = clickData["points"][0]["customdata"][2]
        webbrowser.open_new_tab(url)
    else:
        raise PreventUpdate

app.run(port=8055)
