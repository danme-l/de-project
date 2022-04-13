### Google Bigquery
Serverless Cloud Data Warehouse.

### Data Warehouse
The DWH currently contains two tables; Bixi Trip Data from 2018-2020 as well as a Stations table made from combining the stations files for those three years and discarding the duplicates (see [data/README](/data/README.md) for info).

I used dwh_2020_only.sql to set up the first version with 2020 data only and play around with BigQuery. It won't be used for the final version.

**Current Issues**
At the moment I'm facing the following issue with Partioning the trips data:

```Error while reading table: dauntless-sun-338520.bixi_trips_data.bixi_trips_data, error message: Could not parse 'MTL-ECO5.1-01' as INT64 for field start_station_code (position 1) starting at location 41484514 with message 'Unable to parse'```

It appears there is some record in the stations column for one of those years that is incorrect. For some reason, BQ allows me to insert the record into a non-partitioned table but not the main one. To be addressed this week.