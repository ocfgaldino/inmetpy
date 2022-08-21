# import os, sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import unittest

from ..inmetpy.stations import InmetStation

# class TestInmetStation(unittest.TestCase):
    
#     def test_get_auto_stations(self):
        
#         col_names = ['CD_OSCAR',
#                      'STATION_NAME',
#                      'FL_CAPITAL',
#                      'END_DATE_OPERATION',
#                      'CD_SITUATION',
#                      'TP_STATION',
#                      'LATITUDE',
#                      'CD_WSI',
#                      'CD_DISTRICT',
#                      'HEIGHT',
#                      'STATE',
#                      'INSTITUTE',
#                      'CD_STATION',
#                      'LONGITUDE',
#                      'START_DATE_OPERATION']
        
#         api = InmetStation()
#         stations = api.get_auto_stations()
#         col_names_stations = stations.columns.tolist()
#         self.assertEqual(col_names_stations, col_names)
        
#     def test_get_all_stations_wrong_date_format(self):
        
#         api = InmetStation()
#         self.assertRaises(ValueError, api.get_all_stations,"2021/05/01")
        
        
#     def test_filter_state(self):
        
#         api = InmetStation()
#         self.assertRaises(ValueError, api.search_station_by_state, ["SS"])

        
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

        

        
        
    
    


# if __name__ == "__main__":
#     unittest.main()