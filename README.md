[![PyPI version](https://badge.fury.io/py/inmetpy.svg)](https://badge.fury.io/py/inmetpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/inmetpy?color=blue)
![PyPI - License](https://img.shields.io/pypi/l/inmetpy)
[![Build](https://github.com/ocfgaldino/inmetpy/actions/workflows/inmetpy.yml/badge.svg)](https://github.com/ocfgaldino/inmetpy/actions/workflows/inmetpy.yml)

# InmetPy - A Python API Client for the Brazilian National Institute of Meteorology - INMet



> :warning: **Package development in progress!** 


*This is an **unofficial** (from INMET) python package for the INMET API.*


- Get all stations over Brazil (Manual and Automatic);
- Get historical data for each station;
- Search the stations near by at given location;

# Install

Install using pip

```bash
pip install inmetpy
```

# Methods
- get_stations: Get a list of details of all stations available at INMET API.
- get_all_stations: get data from all stations at given date;
- get_data_station: get data for a list of stations for a given date interval;
- search_station_by_state: search for all stations available for a given state(s);
- search_station_by_coords: search the closest *n* stations available for a given coordinate (latitude, longitude); 



# Comand Line Library Usage

```bash
# get data from all inmet station after a selected date
inmetpy get_all_stations 2021-09-01

# get data from a station or a list of stations
inmetpy get_data_station 2021-09-01 2021-09-10 '[A652,A667]'
```

# Basic usage

## To start the API.

```python
from inmetpy.stations import InmetStation
inmet = InmetStation()
```

## List stations

Once the inmetpy is initialzed, all stations details are loaded. To get a dataframe with all stations:

```python
stations = inmet.stations()
```

The INMET has two types of meteorological stations, automatic and traditional stations. Traditional stations are basically manual stations, so in inmetPy is possible to filter a specific type with "A" or "M" when the station method is called. 

```python
automatic_stations = inmet.stations("A") # All automatic stations
manual_stations = inmet.stations("M") # All manual/traditional stations
```

### Seach stations 

It is possible to seach by stations at specific state(s) or near by a specific coordinate, using the methods `search_station_by_state` and `search_station_by_coords`. 

```python
states = ['RJ','SP','MG','BA']
stations = inmet.search_station_by_state(states)
```

To use the a central coordinate to search the closest `n` stations:

```python
# Brasilia coordinates
lat = -15.7975
lon = -47.8919

stations = inmet.search_station_by_coords(lat=lat, lon=lon, n_stations = 5)
# It returns the 5 closest stations of lat,lon. The dataframe returned contains a new attribute `DISTANCE`, with the distance of that stations of lat,lon, in kilometers.

```

It is also possible to filter the station type using `station_type` on the methods above.

---

### Get data from stations

To request data from stations, there are 3 methods. `get_all_stations`, which request all data from all stations for a specific date (the current day is the default). `get_data_station` request data from specific stations within a time range period. In this case, the data can be request in two time resolutions: `hourly` or `daily`.

```python
# To request data from the current moment
weather_data = inmet.get_all_stations() 

# To request data for specific day, YYYY-MM-DD
weather_data = inmet.get_all_stations('2021-01-01') 

```



```python
# import the library
from inmetpy.stations import InmetStation
inmet = InmetStation()

# list all inmet stations available
stations = inmet.get_stations() # get details of all stations available

auto_stations = inmet.get_stations("A") # details of all automatic stations
manual_stations = inmet.get_stations("M") # details of all manual stations

# get data from all inmet station after a selected date
inmet.get_all_stations(date) # date in format YYYY-MM-DD"

# get data from a station or a list of stations
inmet.get_data_station(start_date, end_date, by, station_id) # stations must be a list of strings with the "CD_STATION" (ID) of the stations desired.
```
