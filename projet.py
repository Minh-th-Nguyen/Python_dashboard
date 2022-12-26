import pandas as pd
import dash
import plotly
import matplotlib.pyplot as plt
import folium
import numpy as np
import geopandas as gpd

"""#import data
data = pd.read_csv('Data.csv', sep = ';')
for i in range(2019,2022) :
    data[data['rentree_scolaire'] == i].hist(column = 'nombre_total_eleves', bins = data[data['rentree_scolaire'] == i]['nombre_total_eleves'].max(), grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
    print(data[data['rentree_scolaire'] == i]['nombre_total_eleves'].sum())
plt.show()"""

def generate_map(year, data):

    data = data[data['rentree_scolaire'] == year]

    map = folium.Map(location=[46, 2.6750], zoom_start = 7, tiles="cartodbpositron")   
    regions_data = data.drop(['rentree_scolaire', 'academie', 'departement', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri', 'code_postal'], axis=1)
    regions_data = regions_data.groupby(['region_academique']).agg({'region_academique' : 'first','nombre_total_eleves' : 'mean'})
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

    folium.Choropleth(
    geo_data='regions.geojson',
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

    geo_data = gpd.read_file('regions.geojson')
    geo_data.rename(columns={"nom" : "region_academique"}, inplace=True)
    regions_data.reset_index(drop = True, inplace=True)
    geo_data = geo_data.merge(regions_data, on="region_academique")
    geo_data['nombre_total_eleves'] = geo_data['nombre_total_eleves'].astype('int')    

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    region = folium.features.GeoJson(
        geo_data,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields = ["region_academique", "nombre_total_eleves"],
            aliases=['Région :', "nombre d'eleves moyen par école"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )
    region_layer.add_child(region)
    map.add_child(region_layer)
    map.keep_in_front(region_layer)

    departements_data = data.drop(['rentree_scolaire', 'academie', 'region_academique', 'commune', 'numero_ecole', 'denomination_principale', 'patronyme', 'secteur', 'rep', 'rep_plus', 'tri'], axis=1)
    departements_data = departements_data.groupby(['departement']).agg({'departement' : 'first', 'code_postal' : 'first', 'nombre_total_eleves' : 'mean'})
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

    departement = folium.Choropleth(
    geo_data='departements.geojson',
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

    geo_departement_data = gpd.read_file('departements.geojson')
    geo_departement_data.rename(columns={"code" : "departement_number"}, inplace=True)
    geo_departement_data = geo_departement_data.merge(departements_data, on="departement_number")
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
    region = folium.features.GeoJson(
        geo_departement_data,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields = ["departement", "nombre_total_eleves"],
            aliases=['departement :', "nombre d'eleves moyen par école"],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        )
    )
    departement_layer.add_child(region)
    map.add_child(departement_layer)
    map.keep_in_front(departement_layer)
    map.add_child(folium.LayerControl())

    map.save("map" + str(year) + ".html")

def map() :
    data = pd.read_csv('Data.csv', sep = ';')
    for i in range(2019,2022) :
        generate_map(i, data)

if __name__ == "__main__" :
    map()