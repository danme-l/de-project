-- Create external table from GCS
-- This is a 2020 table only for initial testing purposes
CREATE OR REPLACE EXTERNAL TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_2020`
OPTIONS (
    format = 'csv',
    uris = ['gs://data_lake_bucket_dauntless-sun-338520/raw/OD_2020.csv']
);

-- Create a Partitioned table over the pickup date
CREATE OR REPLACE TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_2020_partitioned`
PARTITION BY 
    DATE(start_date) AS 
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_2020`;

-- stations table
CREATE OR REPLACE EXTERNAL TABLE `dauntless-sun-338520.bixi_trips_data.bixi_stations_2020`
OPTIONS (
    format = 'csv',
    uris = ['gs://data_lake_bucket_dauntless-sun-338520/raw/stations.csv']
);

-- Check the table
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_2020` LIMIT 20;

-- which start stations had the longest trips in July?
SELECT trips.duration_sec, stations.name 
FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_2020_partitioned` trips, `dauntless-sun-338520.bixi_trips_data.bixi_stations_2020` stations
WHERE DATE(trips.start_date) BETWEEN '2020-07-01' and '2020-07-31'
AND trips.start_station_code = stations.code
ORDER BY trips.duration_sec DESC;




