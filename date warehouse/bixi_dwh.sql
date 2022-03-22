-- Create external table from GCS
-- Trips data sets are sequential, so they'll be added to a single table
CREATE OR REPLACE EXTERNAL TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_data`
OPTIONS (
    format = 'parquet',
    uris = ['gs://data_lake_bucket_dauntless-sun-338520/raw/OD_*.parquet']
);

-- Check
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_data` LIMIT 15;

-- Create a Partitioned table over the pickup date
CREATE OR REPLACE TABLE `dauntless-sun-338520.bixi_trips_data.bixi_trips_partioned`
PARTITION BY 
    DATE(start_date) AS 
SELECT * FROM `dauntless-sun-338520.bixi_trips_data.bixi_trips_data`;