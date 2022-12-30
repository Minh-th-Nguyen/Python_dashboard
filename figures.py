import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import plotly
import matplotlib.pyplot as plt
import folium
import numpy as np
import geopandas as gpd

data = pd.read_csv('resources\Data.csv', sep = ';')

def pie_chart(value):
    global data
    data = data[data['rentree_scolaire'] == value]
    chart_dict = { "Classe" : ["Pré-élémentaire","CP", "CE1", "CE2", "CM1", "CM2"], "nombre d'élève" : [data["nombre_eleves_preelementaire_hors_ulis"].sum(), 
    data["nombre_eleves_cp_hors_ulis"].sum(), data["nombre_eleves_ce1_hors_ulis"].sum(), 
    data["nombre_eleves_ce2_hors_ulis"].sum(), data["nombre_eleves_cm1_hors_ulis"].sum(), 
    data["nombre_eleves_cm2_hors_ulis"].sum()]}
    chart_data = pd.DataFrame(data=chart_dict)
    return px.pie(chart_data, hover_name ="Classe",values="nombre d'élève", hole=0.6).update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    })

def histogram(value):
    global data
    return( 
        px.histogram(
            data[data['rentree_scolaire'] == value], 
            x="nombre_total_eleves", 
            nbins = int(data[data['rentree_scolaire'] == value]['nombre_total_eleves'].max()),  
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

    data = data[data['rentree_scolaire'] == year]

    map = folium.Map(location=[46, 2.6750], zoom_start = 7, tiles="cartodbpositron")   
    regions_data = data.drop(['rentree_scolaire', 'academie', 'departement', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri', 'code_postal'], axis=1)
    regions_data = regions_data.groupby(['region_academique']).agg({'region_academique' : 'first', 'nombre_total_classes' : 'mean', 'nombre_total_eleves' : 'mean'})
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

    scale = np.linspace(regions_data['nombre_total_eleves'].min(),
    regions_data['nombre_total_eleves'].max(),
    10, dtype=int)
    scale = scale.tolist()
    scale[-1] = scale[-1]+1

    region_layer = folium.FeatureGroup(name='Région value', show=False)

    geo_data = gpd.read_file("resources/regions.geojson")

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

    geo_data.rename(columns={"nom" : "region_academique"}, inplace=True)
    regions_data.reset_index(drop = True, inplace=True)
    geo_data = geo_data.merge(regions_data, on="region_academique")
    geo_data["nombre d'élève par classe moyen"] = (geo_data['nombre_total_eleves']/geo_data['nombre_total_classes']).astype('int')
    geo_data['nombre_total_eleves'] = geo_data['nombre_total_eleves'].astype('int')

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
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

    departements_data = data.drop(['rentree_scolaire', 'academie', 'region_academique', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri'], axis=1)
    departements_data = departements_data.groupby(['departement']).agg({'departement' : 'first', 'nombre_total_classes' : 'mean', 'code_postal' : 'first', 'nombre_total_eleves' : 'mean'})
    departements_data.reset_index(drop = True, inplace=True)
    departements_data["departement_number"] = departements_data.code_postal.astype(str).str[:2]

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

    scaledep = np.linspace(departements_data['nombre_total_eleves'].min(),
    regions_data['nombre_total_eleves'].max(),
    10, dtype=int)
    scaledep = scaledep.tolist()
    scaledep[-1] = scaledep[-1]+1

    geo_departement_data = gpd.read_file("resources/departements.geojson")

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

    geo_departement_data.rename(columns={"code" : "departement_number"}, inplace=True)
    geo_departement_data = geo_departement_data.merge(departements_data, on="departement_number")
    geo_departement_data["nombre_eleve_moyen_classe"] = (geo_departement_data['nombre_total_eleves']/geo_departement_data['nombre_total_classes']).astype('int')
    geo_departement_data['nombre_total_eleves'] = geo_departement_data['nombre_total_eleves'].astype('int')

    departement_layer = folium.FeatureGroup(name='Département value', show=True)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
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

    map.save("resources\map" + str(year) + ".html")

def map() :
    global data
    for i in range(2019,2022) :
        generate_map(i, data)


def indicator(year, previous_year) :
    global data

    def Calculate_student_percentage(year) : 
        df = data[data['rentree_scolaire'] == year]
        df = df[df['secteur'] == "PUBLIC"]
        return (df['nombre_total_eleves'].sum()*100)/data[data['rentree_scolaire'] == year]['nombre_total_eleves'].sum()

    def Calculate_school_percentage(year) : 
        df = data[data['rentree_scolaire'] == year]
        df = df[df['secteur'] == "PUBLIC"]
        return (len(df.axes[0])*100)/len(data[data['rentree_scolaire'] == year].axes[0])

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = data[data['rentree_scolaire'] == year]['nombre_total_eleves'].sum(),
        title = {"text": "<span style='font-size:1.5em'>Nombre d'élèves<br><br><span style='font-size:0.8em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': data[data['rentree_scolaire'] == previous_year]['nombre_total_eleves'].sum(), 'relative': True},
        domain = {'x': [0, 0.25], 'y': [0.3, 0.7]}
    ))
        

    fig.add_trace(
        go.Indicator(
        mode = "number+delta",
        number = {'suffix': "%"},
        value = Calculate_student_percentage(year),
        title = {"text": "<span style='font-size:1.5em'>Elèves dans le public<br><br><span style='font-size:0.8em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': Calculate_student_percentage(previous_year), 'relative': False},
        domain = {'x': [0.25, 0.5], 'y': [0.3, 0.7]}
        )
    )


    fig.add_trace(
        go.Indicator(
        mode = "number+delta",
        number = {'suffix': "%"},
        value = Calculate_school_percentage(year),
        title = {"text": "<span style='font-size:1.5em'>Ecole publique<br><br><span style='font-size:0.8em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': Calculate_school_percentage(previous_year), 'relative': False},
        domain = {'x': [0.5, 0.75], 'y': [0.3, 0.7]}
        )
    )


    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = len(data[data['rentree_scolaire'] == year].axes[0]),
        title = {"text": "<span style='font-size:1.5em'>Nombre d'écoles<br><br><span style='font-size:0.8em;color:gray'>Delta par rapport à l'année " + str(previous_year) + "</span><br>"},
        delta = {'reference': len(data[data['rentree_scolaire'] == previous_year].axes[0]), 'relative': True},
        domain = {'x': [0.75, 1], 'y': [0.3, 0.7]}
        )
    )

    fig.add_trace(go.Indicator(
        mode = "gauge",
        value = Calculate_student_percentage(year),
        align = "left",
        domain = {'x': [0.32, 0.43], 'y': [0.25, 0.3]},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'bar': {
                'color': "red",
                'thickness': .9,
            },
        },
    ))

    fig.add_trace(go.Indicator(
        mode = "gauge",
        value = Calculate_school_percentage(year),
        align = "left",
        domain = {'x': [0.57, 0.68], 'y': [0.25, 0.3]},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, 100]},
            'bar': {
                'color': "red",
                'thickness': .9,
            },
        },
    ))

    fig.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    })

    return fig


if __name__ == "__main__" :
    test = pie_chart(2021)
    test.show()