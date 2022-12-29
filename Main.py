import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from projet import map, histogram, pie_chart, indicator

previous_value = 2021

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv('Data.csv', sep = ';')

app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "Dashboard"
app.layout = html.Div([
    html.H1("Dashboard Ecole primaire"),

    html.Iframe(
        id = "map", 
        width = '100%', 
        height = '1400'
    ),

    html.Div([    
            html.Label('Année'),
            dcc.Slider(    
                2019, 2021, 1,
                value=2021,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id = "year"
            )
        ],
        style={'width': "100%"}
    ),

    html.Div([ 
        dcc.Graph(
            id="histogram"
        )
    ], style={'width': "100%"}
    ),

    html.Div([ 
            dcc.Graph(
                id="pie chart"
            )
        ],
        style={'width': "100%"}
    ),

    html.Div([ 
            dcc.Graph(
                id="indicator",
            )
        ],
        style={'width': "100%"}
    )

])


@app.callback(
    Output("map", "srcDoc"),
    Input('year', 'value'),
    )
def update_map(value):
    if value is None : 
        return open("map2021.html", 'r').read()
    return open("map" + str(value) + ".html", 'r').read()


@app.callback(
    Output("histogram", "figure"),
    Input('year', 'value')
    )
def update_hist(value):
    return histogram(value)


@app.callback(
    Output("pie chart", "figure"),
    Input('year', 'value')
    )
def update_hist(value):
    return pie_chart(value)


@app.callback(
    Output("indicator", "figure"),
    Input('year', 'value')
    )
def update_indicator(value):
    global previous_value
    temp = previous_value
    previous_value = value
    return indicator(value, temp)


if __name__ == "__main__" :
    map()
    app.run_server(debug=True)