[![PyPI version](https://badge.fury.io/py/inmetpy.svg)](https://badge.fury.io/py/inmetpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/inmetpy?color=blue)
![PyPI - License](https://img.shields.io/pypi/l/inmetpy)
[![Build](https://github.com/ocfgaldino/inmetpy/actions/workflows/inmetpy.yml/badge.svg)](https://github.com/ocfgaldino/inmetpy/actions/workflows/inmetpy.yml)
![Codiga](https://api.codiga.io/project/34449/score/svg)
![!Codiga](https://api.codiga.io/project/34449/status/svg)


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
