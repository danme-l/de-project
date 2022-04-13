import pandas as pd
import os
from google.cloud import storage

# cloud storage bucket name
BUCKET = 'data_lake_bucket_dauntless-sun-338520'

# read in data from the csv files
stations_20 = pd.read_csv('stations.csv')
stations_19 = pd.read_csv('Stations_2019.csv')
stations_18 = pd.read_csv('Stations_2018.csv')

# 2019 code column erroneously spelt with capital
stations_19.rename(columns = {'Code': 'code'}, inplace=True)

stations = pd.concat([stations_18, stations_19, stations_20])
stations = stations.sort_values(by=['code'])
stations = stations.drop_duplicates(subset=['code']).set_index('code')

print(stations.head(12))

stations.to_csv('stations_all.csv')

# upload it to gcs
client = storage.Client()
bucket = client.bucket(BUCKET)
blob = bucket.blob('raw/stations_all')
blob.upload_from_filename('stations_all.csv')