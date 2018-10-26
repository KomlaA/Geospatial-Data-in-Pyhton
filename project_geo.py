# Load all importance packages
import geopandas
import numpy as np
import pandas as pd
from shapely.geometry import Point

import missingno as msn

import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from descartes import PolygonPatch


country = geopandas.read_file("data.json")
country.head()

#print(type(country))
#print(country.head())
#print(country.geometry)
#country[country['NAME'].isin(['Alaska','Hawaii']) == False].plot(figsize=(30,20), color='#3B3C6E')
#plt.show()

florence = pd.read_csv('data_1.csv')
#print(florence.head())
#print(florence.info())

#msn.bar(florence, color = "blue")  #Checking missing values using the missingno package
#plt.show()
#print(florence.describe())

#With any data, you will need to clean up and take only what you need to work with.
#In this case we drop 
florence_1 = florence.drop(['AdvisoryNumber', 'Forecaster','Received'], axis = 1)
#print(florence_1.head())

#ADD "-" in front of the number to correctly plot th data
florence_1['Long'] = 0 - florence_1['Long']
#print(florence_1.head())

#Combining Lattitude and Longitude to create hurricane coordinates
florence_1['coordinates'] = florence_1[['Long', 'Lat']].values.tolist()
#print(florence_1.head())

#Change the coordinates to a GeoPoint
florence_1['coordinates'] = florence_1['coordinates'].apply(Point)
#print(florence_1.head())

#Converting the data into a GeoSpatial Data
florence_1 = geopandas.GeoDataFrame(florence_1, geometry ='coordinates')
print(florence_1.head())

#Visualization / Plotting to see the hurricane overlay the US map

fig, ax = plt.subplots(1,figsize =(30, 20))
base = country[country['NAME'].isin(['Alaska','Hawaii']) == False].plot(figsize=(30,20), color='#3B3C6E')

#Plotting the hurricane position on top with red color
florence_1.plot(ax=base, column ='Wind', marker='<', markersize = 10,
                cmap ='cool', label="Wind Speed(mph)")
_= ax.axis('off')
plt.legend()
ax.set_title("Hurricane Florence in US Map", fontsize=25)
plt.savefig('Hurricane_footage.png', bbox_inches='tight')
plt.show()


