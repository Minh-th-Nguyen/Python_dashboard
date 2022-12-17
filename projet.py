import pandas as pd
import dash
import plotly
import matplotlib.pyplot as plt

#import data
data = pd.read_csv('Data.csv', sep = ';')
for i in range(2019,2022) :
    data[data['rentree_scolaire'] == i].hist(column = 'nombre_total_eleves', bins = data[data['rentree_scolaire'] == i]['nombre_total_eleves'].max(), grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
plt.show()

 