import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from figures import map, histogram, pie_chart, nb_student, student_percentage, school_percentage, nb_school
from resources.Layout import layout

#year for Delta in indicators
previous_value = 2021

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#dash page
app = Dash(__name__, external_stylesheets=stylesheets)
app.title = "Dashboard Ecole"
#create webpage layout (layout is defined in a seperated file)
app.layout = layout()

#callback to update map
@app.callback(
    Output("map", "srcDoc"),
    Input('year', 'value'),
    )
def update_map(value):
    """update map

    Args:
        value (int): year

    Returns:
        (srcdoc): map
    """
    if value is None : 
        return open("resources\map2021.html", 'r').read()
    return open("resources\map" + str(value) + ".html", 'r').read()

#callback to update histogram
@app.callback(
    Output("histogram", "figure"),
    Input('year', 'value')
    )
def update_hist(value):
    """update histogram

    Args:
        value (int): year

    Returns:
        (figure): histogram
    """
    return histogram(value)

#callback to update pie chart
@app.callback(
    Output("pie chart", "figure"),
    Input('year', 'value')
    )
def update_hist(value):
    """update pie chart

    Args:
        value (int): year

    Returns:
        (figure): pie chart
    """
    return pie_chart(value)

#callback to update nb student indicator
@app.callback(
    Output("nb_student", "figure"),
    Input('year', 'value')
    )
def update_nb_student(value):
    """update indicator nb_student

    Args:
        value (int): year

    Returns:
        (figure): indicator
    """
    global previous_value
    return nb_student(value, previous_value)

#callback to update student percentage in public school indicator
@app.callback(
    Output("student_percentage", "figure"),
    Input('year', 'value')
    )
def update_student_percentage(value):
    global previous_value
    return student_percentage(value, previous_value)

#callback to update percentage of public school indicator

@app.callback(
    Output("school_percentage", "figure"),
    Input('year', 'value')
    )
def update_school_percentage(value):
    global previous_value
    return school_percentage(value, previous_value)

#callback to update nb of school
@app.callback(
    Output("nb_school", "figure"),
    Input('year', 'value')
    )
def update_nb_school(value):
    global previous_value
    temp = previous_value
    previous_value = value
    return nb_school(value, temp)

#Main : start dash
if __name__ == "__main__" :
    #create the map and store them in ressources folders 
    map()
    app.run_server(debug=True)

