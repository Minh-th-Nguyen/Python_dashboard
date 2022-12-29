import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from projet import map, histogram, pie_chart, indicator
from Layout import layout

previous_value = 2021

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv('Data.csv', sep = ';')

app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "Dashboard"
app.layout = layout()

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