import numpy as np
import pandas as pd 
pd.set_option('display.max_columns', None)

# python file for general explorations of the data 

april2014 = pd.read_csv("OD_2014-04.csv")
print(april2014.head())

stations2014 = pd.read_csv("Stations_2014.csv")
print(stations2014.head())
