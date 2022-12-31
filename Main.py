import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from figures import map, histogram, pie_chart, nb_student, student_percentage, school_percentage, nb_school
from resources.Layout import layout

previous_value = 2021

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "Dashboard"
app.layout = layout()

@app.callback(
    Output("map", "srcDoc"),
    Input('year', 'value'),
    )
def update_map(value):
    if value is None : 
        return open("resources\map2021.html", 'r').read()
    return open("resources\map" + str(value) + ".html", 'r').read()


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
    Output("nb_student", "figure"),
    Input('year', 'value')
    )
def update_nb_student(value):
    global previous_value
    return nb_student(value, previous_value)

@app.callback(
    Output("student_percentage", "figure"),
    Input('year', 'value')
    )
def update_student_percentage(value):
    global previous_value
    return student_percentage(value, previous_value)

@app.callback(
    Output("school_percentage", "figure"),
    Input('year', 'value')
    )
def update_school_percentage(value):
    global previous_value
    return school_percentage(value, previous_value)

@app.callback(
    Output("nb_school", "figure"),
    Input('year', 'value')
    )
def update_nb_school(value):
    global previous_value
    temp = previous_value
    previous_value = value
    return nb_school(value, temp)


if __name__ == "__main__" :
    map()
    app.run_server(debug=True)