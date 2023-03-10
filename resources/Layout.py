from dash import html, dcc

#return layout
def layout(): 
    return html.Div([
        html.Div([
            html.H1("Dashboard Ecole élémentaire et pré-élémentaire"),
        ], id="title"),

        html.Div([
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
                ),
            ],id="slider",
            ),

            html.Div([ 
                html.Div([ 
                    dcc.RadioItems(
                        ['Par classe', 'Par école'],
                        'Par classe',
                        id='bouton_int',
                        inline=True
                        )
                    ], id="bouton2"),
                ], id="bouton"),
        ]),

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
                html.H2("Comparaison du nombre d'élève par école", id="map_title"),
                html.Div([
                    html.Iframe(id="map")
                ], id="map2")
            ], id="left"),

            html.Div([

                html.H2("Répartition du nombre d'élève par école", id="histogram_title"),

                html.Div([
                    dcc.Graph(
                        id="histogram"
                    ),
                ], id="histogram2"
                ),

                html.H2("Répartition des élèves par classe", id="pie_chart_title"),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id="pie chart"
                        )
                    ], id="pie_chart")
                ], id="pie_chart2"
                ),

            ], id="right")

        ], id="map_histo_pie")

    ],
    style={"overflow": "hidden"}
    )       