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

        
def test_get_data_station(inmet):



        
        
    
    
