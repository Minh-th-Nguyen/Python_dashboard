import pandas as pd
import plotly
from dash import Dash, html, dcc, Input, Output
from projet import map

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "Dashboard"
app.layout = html.Div([
    html.H1("Dashboard Ecole primaire"),
    html.Iframe(
        id = "map", 
        width = '2000', 
        height = '1400'),
    html.Div([    
        html.Label('Année'),
        dcc.Slider(    
            2019, 2021, 1,
            value=2021,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            id = "year"
        )
    ])
])

@app.callback(
    Output("map", "srcDoc"),
    Input('year', 'value'),
    prevent_initial_callback=True
    )
def update_output(value):
    if value is None : 
        return open("map2021.html", 'r').read()
    return open("map" + str(value) + ".html", 'r').read()

if __name__ == "__main__" :
    map()
    app.run_server(debug=True)