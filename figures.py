import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import plotly
import matplotlib.pyplot as plt
import folium
import numpy as np
import geopandas as gpd

#file figures import and transform the data to create figures that will be used in the Main

#raw data
global_data = pd.read_csv('resources\Data.csv', sep = ';')

def pie_chart(value):
    """create pie chart

    Args:
        value (int) : year

    Returns:
        figure pie chart
    """
    global global_data

    #transform data to have a dataframe of all classes and numbers of student in each classes
    data = global_data[global_data['rentree_scolaire'] == value]
    chart_dict = { "Classe" : ["Pré-élémentaire", "CP", "CE1", "CE2", "CM1", "CM2"], 
    "nombre d'élève" : [data["nombre_eleves_preelementaire_hors_ulis"].sum(), 
    data["nombre_eleves_cp_hors_ulis"].sum(), data["nombre_eleves_ce1_hors_ulis"].sum(), 
    data["nombre_eleves_ce2_hors_ulis"].sum(), data["nombre_eleves_cm1_hors_ulis"].sum(), 
    data["nombre_eleves_cm2_hors_ulis"].sum()]}
    chart_data = pd.DataFrame(data=chart_dict)

    #create the pie chart
    return px.pie(chart_data, names="Classe", hover_name ="Classe",values="nombre d'élève", hole=0.6).update_layout({
        "height" : 400,
        "margin" : dict(t=20, b=10),
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    })

def histogram(value):
    """create histogram

    Args:
        value (int) : year
    Returns:
        figure histogram
    """
    global global_data
    return( 
        px.histogram(
            global_data[global_data['rentree_scolaire'] == value], 
            x="nombre_total_eleves", 
            nbins = int(global_data[global_data['rentree_scolaire'] == value]['nombre_total_eleves'].max()),  
            labels={"nombre_total_eleves" : "nombre d'élève"},
            ).update_layout(
            yaxis_title="nombre d'école",
            bargap=0.2,
    ).update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    })
)

def generate_map(year, data):
    """create a map for a specific year

    Args:
        year (int): year
        data (dataframe): data

    save:
        map
    """

    data = global_data[global_data['rentree_scolaire'] == year]

    #create empty map
    map = folium.Map(location=[46, 2.6750], zoom_start = 6, tiles="cartodbpositron")   

    #rework data to have number of student in each school
    regions_data = data.drop(['rentree_scolaire', 'academie', 'departement', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri', 'code_postal'], axis=1)
    regions_data = regions_data.groupby(['region_academique']).agg({'region_academique' : 'first', 'nombre_total_classes' : 'mean', 'nombre_total_eleves' : 'mean'})
   
    #rework data due to mismatch in name between geo.json and raw data
    regions_data.loc[(regions_data.region_academique == 'AUVERGNE-ET-RHONE-ALPES'),'region_academique'] = 'Auvergne-Rh\u00f4ne-Alpes'
    regions_data.loc[(regions_data.region_academique == 'BOURGOGNE-ET-FRANCHE-COMTE'),'region_academique'] = 'Bourgogne-Franche-Comt\u00e9'
    regions_data.loc[(regions_data.region_academique == 'BRETAGNE'),'region_academique'] = 'Bretagne'
    regions_data.loc[(regions_data.region_academique == 'CENTRE-VAL-DE-LOIRE'),'region_academique'] = 'Centre-Val de Loire'
    regions_data.loc[(regions_data.region_academique == 'CORSE'),'region_academique'] = 'Corse'
    regions_data.loc[(regions_data.region_academique == 'GRAND-EST'),'region_academique'] = 'Grand Est'
    regions_data.loc[(regions_data.region_academique == 'GUADELOUPE'),'region_academique'] = 'Guadeloupe'
    regions_data.loc[(regions_data.region_academique == 'GUYANE'),'region_academique'] = 'Guyane'
    regions_data.loc[(regions_data.region_academique == 'HAUTS-DE-FRANCE'),'region_academique'] = 'Hauts-de-France'
    regions_data.loc[(regions_data.region_academique == 'ILE-DE-FRANCE'),'region_academique'] = '\u00cele-de-France'
    regions_data.loc[(regions_data.region_academique == 'LA-REUNION'),'region_academique'] = 'La R\u00e9union'
    regions_data.loc[(regions_data.region_academique == 'MARTINIQUE'),'region_academique'] = 'Martinique'
    regions_data.loc[(regions_data.region_academique == 'MAYOTTE'),'region_academique'] = 'Mayotte'
    regions_data.loc[(regions_data.region_academique == 'NORMANDIE'),'region_academique'] = 'Normandie'
    regions_data.loc[(regions_data.region_academique == 'NOUVELLE-AQUITAINE'),'region_academique'] = 'Nouvelle-Aquitaine'
    regions_data.loc[(regions_data.region_academique == 'OCCITANIE'),'region_academique'] = 'Occitanie'
    regions_data.loc[(regions_data.region_academique == 'PAYS-DE-LA-LOIRE'),'region_academique'] = 'Pays de la Loire'
    regions_data.loc[(regions_data.region_academique == "PROVENCE-ALPES-COTE-D'AZUR"),'region_academique'] = "Provence-Alpes-C\u00f4te d'Azur"

    #create scale base on the data
    scale = np.linspace(regions_data['nombre_total_eleves'].min(),
    regions_data['nombre_total_eleves'].max(),
    10, dtype=int)
    scale = scale.tolist()
    scale[-1] = scale[-1]+1

    #define layer for region's data
    region_layer = folium.FeatureGroup(name='Région value', show=False)

    #geojson of region
    geo_data = gpd.read_file("resources/regions.geojson")

    #create choropleth and add it to the map
    folium.Choropleth(
    geo_data=geo_data,
    data=regions_data,
    columns=['region_academique', 'nombre_total_eleves'],
    key_on='properties.nom',
    fill_color="YlGn",
    threshold_scale = scale,
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name="nombre d'eleves moyen par école (région)",
    highlight=True,
    show=False,
    overlay=True,
    name="Région",
    ).add_to(map)

    #create new dataframe containing data and coordinate
    geo_data.rename(columns={"nom" : "region_academique"}, inplace=True)
    regions_data.reset_index(drop = True, inplace=True)
    geo_data = geo_data.merge(regions_data, on="region_academique")
    geo_data["nombre d'élève par classe moyen"] = (geo_data['nombre_total_eleves']/geo_data['nombre_total_classes']).astype('int')
    geo_data['nombre_total_eleves'] = geo_data['nombre_total_eleves'].astype('int')

    #define style for pop up windows
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}

    #add pop up to the map
    region_value = folium.features.GeoJson(
        geo_data,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields = ["region_academique", "nombre_total_eleves", "nombre d'élève par classe moyen"],
            aliases=['Région', "Nombre d'élèves moyen par école", "Nombre d'eleves moyen par classe"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )
    region_layer.add_child(region_value)
    map.add_child(region_layer)
    map.keep_in_front(region_layer)

    #rework data
    departements_data = data.drop(['rentree_scolaire', 'academie', 'region_academique', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri'], axis=1)
    departements_data = departements_data.groupby(['departement']).agg({'departement' : 'first', 'nombre_total_classes' : 'mean', 'code_postal' : 'first', 'nombre_total_eleves' : 'mean'})
    departements_data.reset_index(drop = True, inplace=True)
    departements_data["departement_number"] = departements_data.code_postal.astype(str).str[:2]

    #rework data due to mismatch in name between geo.json and raw data
    departements_data.loc[(departements_data.departement == 'CORSE-DU-SUD'),'departement_number'] = '2A'
    departements_data.loc[(departements_data.departement == 'HAUTE-CORSE'),'departement_number'] = '2B'
    departements_data.loc[(departements_data.departement == 'AIN'),'departement_number'] = '01'
    departements_data.loc[(departements_data.departement == 'AISNE'),'departement_number'] = '02'
    departements_data.loc[(departements_data.departement == 'ALLIER'),'departement_number'] = '03'
    departements_data.loc[(departements_data.departement == 'ALPES-DE-HTE-PROVENCE'),'departement_number'] = '04'
    departements_data.loc[(departements_data.departement == 'HAUTES-ALPES'),'departement_number'] = '05'
    departements_data.loc[(departements_data.departement == 'ALPES-MARITIMES'),'departement_number'] = '06'
    departements_data.loc[(departements_data.departement == 'ARDECHE'),'departement_number'] = '07'
    departements_data.loc[(departements_data.departement == 'ARDENNES'),'departement_number'] = '08'
    departements_data.loc[(departements_data.departement == 'ARIEGE'),'departement_number'] = '09'

    #create scale
    scaledep = np.linspace(departements_data['nombre_total_eleves'].min(),
    regions_data['nombre_total_eleves'].max(),
    10, dtype=int)
    scaledep = scaledep.tolist()
    scaledep[-1] = scaledep[-1]+1

    #read geojson
    geo_departement_data = gpd.read_file("resources/departements.geojson")

    #create choropleth and add to map
    departement = folium.Choropleth(
    geo_data=geo_departement_data,
    data=departements_data,
    columns=['departement_number', 'nombre_total_eleves'],
    key_on='properties.code',
    threshold_scale = scaledep,
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name="nombre d'eleves moyen par école (département)",
    highlight=True,
    show=True,
    overlay=True,
    name="Département"
    )
    map.add_child(departement)

    #create dataframe containing geojson and data
    geo_departement_data.rename(columns={"code" : "departement_number"}, inplace=True)
    geo_departement_data = geo_departement_data.merge(departements_data, on="departement_number")
    geo_departement_data["nombre_eleve_moyen_classe"] = (geo_departement_data['nombre_total_eleves']/geo_departement_data['nombre_total_classes']).astype('int')
    geo_departement_data['nombre_total_eleves'] = geo_departement_data['nombre_total_eleves'].astype('int')

    #layer for departement data
    departement_layer = folium.FeatureGroup(name='Département value', show=True)

    #add pop up to the map
    departement_value = folium.features.GeoJson(
        geo_departement_data,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields = ["nom", "nombre_total_eleves", "nombre_eleve_moyen_classe"],
            aliases=['Département', "Nombre d'élèves moyen par école", "Nombre d'élèves moyen par classe"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )
    departement_layer.add_child(departement_value)
    map.add_child(departement_layer)
    map.keep_in_front(departement_layer)
    map.add_child(folium.LayerControl())

    #save map in resources and name it depending on the year 
    map.save("resources\map" + str(year) + ".html")


def map() :
    """create map for each year
    """
    global global_data
    for i in range(2019,2022) :
        generate_map(i, global_data)


def nb_student(year, previous_year) :
    """create indicator for nb student

    Args:
        year (int): year
        previous_year (int): previous year selected by user

    Returns:
        figure : indicator nb of students
    """
    global global_data
    data = global_data

    #indicator
    fig = go.Figure(go.Indicator(
    mode = "number+delta",
    number = {"font":{"size":50}},
    value = data[data['rentree_scolaire'] == year]['nombre_total_eleves'].sum(),
    title = {"text": "<span style='font-size:1.5em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
    delta = {'reference': data[data['rentree_scolaire'] == previous_year]['nombre_total_eleves'].sum(), 'relative': True},
    domain = {'x': [0, 1], 'y': [0.3, 0.7]}
    ))

    #transparent background and define size
    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "height" : 200,
    "margin" : dict(t=80),
    })

    return fig


def student_percentage(year, previous_year) :
    """create indicator for percentage of student in public school

    Args:
        year (int): year
        previous_year (int): previous year selected by user

    Returns:
        figure : indicator for percentage of student in public school
    """ 

    global global_data
    data = global_data

    #calculate percentage of student in public school
    def Calculate_student_percentage(year) : 
        df = data[data['rentree_scolaire'] == year]
        df = df[df['secteur'] == "PUBLIC"]
        return (df['nombre_total_eleves'].sum()*100)/data[data['rentree_scolaire'] == year]['nombre_total_eleves'].sum()

    #create indicator
    fig = go.Figure(
    go.Indicator(
    mode = "number+delta",
    number = {'suffix': "%", "font":{"size":50}},
    value = Calculate_student_percentage(year),
    title = {"text": "<span style='font-size:1.5em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
    delta = {'reference': Calculate_student_percentage(previous_year), 'relative': False},
    domain = {'x': [0, 1], 'y': [0.3, 0.7]}
        )
    )

    #create gauge indicator
    fig.add_trace(go.Indicator(
        mode = "gauge",
        value = Calculate_student_percentage(year),
        align = "left",
        domain = {'x': [0.1, 0.9], 'y': [0.1, 0.17]},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'bar': {
                'color': "red",
                'thickness': .9,
            },
        },
    ))

    #transparent background and define size
    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "height" : 200,
    "margin" : dict(t=20, b=20),
    })

    return fig


def school_percentage(year, previous_year) :
    """create indicator for percentage of public school

    Args:
        year (int): year
        previous_year (int): previous year selected by user

    Returns:
        figure : indicator for percentage of public school
    """ 

    global global_data
    data = global_data

    #calculate percentage of public school
    def Calculate_school_percentage(year) : 
        df = data[data['rentree_scolaire'] == year]
        df = df[df['secteur'] == "PUBLIC"]
        return (len(df.axes[0])*100)/len(data[data['rentree_scolaire'] == year].axes[0])        

    #create indicator
    fig = go.Figure(
        go.Indicator(
        mode = "number+delta",
        number = {'suffix': "%", "font":{"size":50}},
        value = Calculate_school_percentage(year),
        title = {"text": "<span style='font-size:1.5em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': Calculate_school_percentage(previous_year), 'relative': False},
        domain = {'x': [0, 1], 'y': [0.3, 0.7]}
        )
    )

    #create gauge
    fig.add_trace(go.Indicator(
        mode = "gauge",
        value = Calculate_school_percentage(year),
        align = "left",
        domain = {'x': [0.1, 0.9], 'y': [0.1, 0.17]},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'bar': {
                'color': "red",
                'thickness': .9,
            },
        },
    ))

    #transparent background and define size
    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "height" : 200,
    "margin" : dict(t=20, b=20),
    })

    return fig


def nb_school(year, previous_year) :
    """create indicator for number of school

    Args:
        year (int): year
        previous_year (int): previous year selected by user

    Returns:
        figure : indicator for number of school
    """ 

    global global_data
    data = global_data

    #create indicator
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        number = {"font":{"size":50}},
        value = len(data[data['rentree_scolaire'] == year].axes[0]),
        title = {"text": "<span style='font-size:1.5em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': len(data[data['rentree_scolaire'] == previous_year].axes[0]), 'relative': True},
        domain = {'x': [0, 1], 'y': [0.3, 0.7]}
        )
    )

    #transparent background and size
    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "height" : 200,
    "margin" : dict(t=80),
    })

    return fig
    