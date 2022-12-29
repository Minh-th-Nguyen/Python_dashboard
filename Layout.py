from dash import html, dcc

def layout(): 
    return html.Div([
        html.H1("Dashboard Ecole primaire"),

        html.Div([    
            html.Label('Année'),
            dcc.Slider(    
                2019, 2021, 1,
                value=2021,
                marks={
                    2019 : "2019",
                    2020 : "2020",
                    2021 : "2021",
                },
                tooltip={"placement": "bottom", "always_visible": True},
                id = "year"
                )
            ],
            style={'width': "30%", 'margin-left': '1000px', "transform": "scale(2)", "margin-top" : "100px"}
        ),

        html.Div([ 
                dcc.Graph(
                    id="indicator",
                )
            ],
            style={'width': "100%"}
        ),

        html.Div([  
            html.Div([  
                html.Iframe(
                    id = "map", 
                    width = '100%', 
                    height = '1000', 
                ),
            ],
            style={'width': "60%", "display": "inline-block"}
            ),
            html.Div([ 
                    html.Div([ 
                        dcc.Graph(
                            id="histogram"
                        )
                    ], 
                    style={'width': "100%"}
                    ),

                    html.Div([ 
                        dcc.Graph(
                            id="pie chart"
                        )
                    ],
                    style={'width': "100%"}
                    ),
            ],
            style={'width': "40%", "display": "inline-block"}
            )
        ]
        ),

    ])