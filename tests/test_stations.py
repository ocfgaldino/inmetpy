from ..inmetpy.stations import InmetStation
        
import pytest  

@pytest.fixture
def inmet():
    return InmetStation()

def test_get_stations_attributes(inmet):

    cols = ['CD_OSCAR', 'STATION_NAME', 'CD_STATION', 'TP_STATION',
       'START_DATE_OPERATION', 'END_DATE_OPERATION', 'LONGITUDE', 'LATITUDE',
       'HEIGHT', 'CD_SITUATION', 'CD_WSI', 'IS_CAPITAL', 'CD_DISTRICT',
       'INSTITUTE', 'STATE']
    
    assert inmet.get_stations().columns.tolist() == cols

def test_get_all_stations_attributes(inmet):

    cols = ['WDIR', 'DATE', 'STATION_NAME', 'RAIN', 'PRES', 'LAT', 'MIN_PRES',
       'MAX_RH', 'MAX_PRES', 'WSPD', 'ST', 'MIN_DWPT', 'MAX_TEMP', 'GLO_RAD',
       'DWPT', 'WGST', 'TEMP', 'HUMI', 'STATION_ID', 'MIN_TEMP', 'LONG',
       'TIME', 'MIN_RH', 'MAX_DWPT']

    assert inmet.get_all_stations().columns.tolist() == cols

        
def test_get_data_station_wrong_input_date(inmet):
    with pytest.raises(ValueError, match = "Incorrect date format, date should be in 'YYYY-MM-DD' format."):
        inmet.get_data_station("12-11-2021", "14-11-2021", "hour", ['A701'])


def test_get_data_station_wrong_input_time_resolution(inmet):
    with pytest.raises(ValueError, match = "Wrong time resolution. by should be 'hour' or 'day'."):
        inmet.get_data_station("2021-01-01", "2021-02-01", "month", ['A701'])


def test_get_data_station_wrong_input_station_id_type(inmet):
    with pytest.raises(TypeError, match = "'station_id should be list.'"):
        inmet.get_data_station("2021-01-01", "2021-02-01", "day", 'A701')


def test_get_data_station_wrong_station_id(inmet):

    stations_id = ['A701','A7124'] #First = Real Station, Last = Fake station
    with pytest.raises(ValueError) as exe_info:
        inmet.get_data_station("2021-01-01", "2021-02-01", "day", stations_id)
        assert exe_info.value == 'There is no station(s): "A7124"'

def test_search_station_by_state_wrong_state(inmet):
    
    states = ['SP','TT']
    with pytest.raises(ValueError) as exe_info:
        inmet.search_station_by_state(states)
        assert exe_info.value == 'There is no state(s): "TT"'

def test_search_station_by_state_wrong_type_station(inmet):
    
    states = ['SP','RJ']
    with pytest.raises(ValueError) as exe_info:
        inmet.search_station_by_state(states, "Auto")
        assert exe_info.value == 'station_type must be either "A" (Automatic), "M" (Manual) or "ALL" (All stations)"'

def test_search_station_by_coords_wrong_coords_type(inmet):

    lat = '-22.44'
    lon = '-24.44'
    with pytest.raises(TypeError) as exe_info:
        inmet.search_station_by_coords(lat, lon)
        assert exe_info.value == "Coordinates (lat,lon) values must be type 'float'"






        
        
    
    
