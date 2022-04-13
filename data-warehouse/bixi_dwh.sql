-- Create external table from GCS
-- Trips data sets are sequential, so they'll be added to a single table
CREATE OR REPLACE EXTERNAL TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_data`
OPTIONS (
    format = 'csv',
    uris = ['gs://data_lake_bucket_dauntless-sun-338520/raw/OD_*.csv']
);


-- stations table 
-- the stations were joined from over the years in a python script
CREATE OR REPLACE EXTERNAL TABLE `dauntless-sun-338520.bixi_trips_data.bixi_stations`
OPTIONS (
    format = 'csv',
    uris = ['gs://data_lake_bucket_dauntless-sun-338520/raw/stations_all']
);

-- Check
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_data` LIMIT 15;

-- Create a Partitioned table over the pickup date
-- this doesn't work yet. view README
CREATE OR REPLACE TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_partioned`
PARTITION BY 
    DATE(start_date) AS 
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_data`;

-- Count by year
SELECT EXTRACT(year FROM trips.start_date) AS year, COUNT(*)
FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_partioned` trips;