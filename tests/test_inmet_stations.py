import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from inmetpy.inmet_stations import InmetStation

class TestInmetStation(unittest.TestCase):
    
    def test_get_auto_stations(self):
        
        col_names = ['CD_OSCAR',
                     'STATION_NAME',
                     'FL_CAPITAL',
                     'END_DATE_OPERATION',
                     'CD_SITUATION',
                     'TP_STATION',
                     'LATITUDE',
                     'CD_WSI',
                     'CD_DISTRICT',
                     'HEIGHT',
                     'STATE',
                     'INSTITUTE',
                     'CD_STATION',
                     'LONGITUDE',
                     'START_DATE_OPERATION']
        
        api = InmetStation()
        stations = api.get_auto_stations()
        col_names_stations = stations.columns.tolist()
        self.assertEqual(col_names_stations, col_names)
        
    def test_get_all_stations_wrong_date_format(self):
        
        api = InmetStation()
        self.assertRaises(ValueError, api.get_all_stations,"2021/05/01")
        
        
    def test_filter_state(self):
        
        api = InmetStation()
        self.assertRaises(ValueError, api.search_station_by_state, ["SS"])

        
        
        
        
        
    
        
        
    
    


if __name__ == "__main__":
    unittest.main()