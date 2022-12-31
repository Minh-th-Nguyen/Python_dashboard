from dash import html, dcc

def layout(): 
    return html.Div([
        html.Div([
            html.H1("Dashboard Ecole primaire, élémentaire et pré-élémentaire"),
        ], id="title"),

        html.Div([ 
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
                #style={'width': "30%", 'margin-left': '1000px', "transform": "scale(2)", "margin-top" : "100px", "zIndex" : 10}
            ),
        ],id="slider",
        ),

        html.Div([ 
                html.Div([
                html.Div([html.H2("Nombre d'élèves")], id="nb_student_title"),
                html.Div([
                dcc.Graph(
                    id="nb_student",
                ),],id="nb_student2",
                ),
                ],style={'width': "22%", "display": "inline-block"}),

                html.Div([
                html.Div([html.H2("Elèves en école public")], id="student_percentage_title"),
                html.Div([
                dcc.Graph(
                    id="student_percentage",
                ),],id="student_percentage2",
                )],
                style={'width': "22%", "display": "inline-block"}),

                html.Div([
                html.Div([html.H2("Ecoles public")], id="school_percentage_title"),
                html.Div([
                dcc.Graph(
                    id="school_percentage",
                ),],id="school_percentage2",
                )],
                style={'width': "22%", "display": "inline-block"}),

                html.Div([
                html.Div([html.H2("Nombre d'écoles")], id="nb_school_title"),
                html.Div([
                dcc.Graph(
                    id="nb_school",
                ),],id="nb_school2",
                )],
                style={'width': "22%", "display": "inline-block"}),
            ],
            id="indicators",
        ),

        html.Div([
            html.Div([
                html.H2("Nombre d'écoles", id="map_title"),
                html.Div([
                    html.Iframe(id="map")
                ], id="map2")
            ], id="left"),

            html.Div([

                html.H2("Nombre d'écoles", id="histogram_title"),

                html.Div([
                    dcc.Graph(
                        id="histogram"
                    ),
                ], id="histogram2"
                ),

                html.H2("Nombre d'écoles", id="pie_chart_title"),

                html.Div([
                    dcc.Graph(
                        id="pie chart"
                    )
                ], id="pie_chart2"
                ),

            ], id="right")

        ], id="map_histo_pie")

    ],
    style={"overflow": "hidden"}
    )       