[![PyPI version](https://badge.fury.io/py/inmetpy.svg)](https://badge.fury.io/py/inmetpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/inmetpy?color=blue)
![PyPI - License](https://img.shields.io/pypi/l/inmetpy)

# InmetPy - A Python API Client for the Brazilian National Institute of Meteorology - INMet

*This is an **unofficial** (from INMET) python package for the INMET API.*


- Get all stations over Brazil (Manual and Automatic);
- Get historical data for each station;
- Search the stations near by at given location;

# Install

Install using pip

```bash
pip install inmetpy
```



# Comand Line Library Usage

```bash
# download a list of inmet stations
inmetpy list_stations "A"

# get data from all inmet station after a selected date
inmetpy get_all_stations 2021-09-01

# get data from a station or a list of stations
inmetpy get_data_station 2021-09-01 2021-09-10 '[A652,A667]'
```

# Library Usage

```bash
# import the library
from inmetpy.inmet_stations import InmetStation
inmet = InmetStation()

# list all inmet stations available
stations = inmet.stations # get details of all stations available

auto_stations = inmet.get_auto_stations() # details of all automatic stations
manual_stations = inmet.get_manual_stations() # details of all manual stations

# get data from all inmet station after a selected date
inmet.get_all_stations(date) # date in format YYYY-MM-DD"

# get data from a station or a list of stations
inmet.get_data_station(start_date, end_date, by, station_id) # stations must be a string or a list of strings of the "CD_STATION" ID of the stations you want
```
