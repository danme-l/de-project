### Data
fetchData.sh is a bash script to download and unzip the files from [the source](https://bixi.com/en/open-data). Some are in subdirectoriess and some aren't. 

The trips data is structured as follows:
| start_date       | start_station_code | end_date         | end_station_code | duration_sec | is_member |
|------------------|--------------------|------------------|------------------|--------------|-----------|
| 2016-04-15 00:00 | 6315               | 2016-04-15 00:05 | 6315             | 349          | 1         |
| 2016-04-15 00:00 | 6019               | 2016-04-15 00:29 | 6347             | 1720         | 1         |
| 2016-04-15 00:00 | 6219               | 2016-04-15 00:29 | 6219             | 284          | 1         |
| 2016-04-15 00:03 | 6211               | 2016-04-15 00:07 | 6307             | 238          | 1         |
| 2016-04-15 00:04 | 6312               | 2016-04-15 00:19 | 6312             | 910          | 1         |

And the station data:
| code | name                     | latitude          | longitude          |
|------|--------------------------|-------------------|--------------------|
| 6209 | Milton / Clark           | 45.51252          | -73.57062          |
| 6436 | Côte St-Antoine / Clarke | 45.48645209646392 | -73.59523415565491 |
| 6214 | Square St-Louis          | 45.51735          | -73.56906          |

These examples are both taken from the 2014 data.