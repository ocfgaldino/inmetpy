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


def test_get_data_station_wrong_station_id(inmet):

    stations_id = ['A701','A7124'] #First = Real Station, Last = Fake station
    with pytest.raises(ValueError) as exe_info:
        inmet.get_data_station("2021-01-01", "2021-02-01", "day", stations_id)
        assert exe_info.value == 'There is no station(s): "A7124"'




        
        
    
    
