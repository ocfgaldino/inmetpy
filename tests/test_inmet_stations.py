import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from inmetpy.stations.inmet_stations import InmetStation

class TestInmetStation(unittest.TestCase):
    
    def test_list_stations_T(self):
        
        col_names = ['CD_OSCAR',
                     'DC_NOME',
                     'FL_CAPITAL',
                     'DT_FIM_OPERACAO',
                     'CD_SITUACAO',
                     'TP_ESTACAO',
                     'VL_LATITUDE',
                     'CD_WSI',
                     'CD_DISTRITO',
                     'VL_ALTITUDE',
                     'SG_ESTADO',
                     'SG_ENTIDADE',
                     'CD_ESTACAO',
                     'VL_LONGITUDE',
                     'DT_INICIO_OPERACAO']
        
        api = InmetStation()
        stations = api.list_stations("T")
        col_names_stations = stations.columns.tolist()
        self.assertEqual(col_names_stations, col_names)
        
        
    def test_list_stations_M(self):
        col_names = ['CD_OSCAR',
                     'DC_NOME',
                     'FL_CAPITAL',
                     'DT_FIM_OPERACAO',
                     'CD_SITUACAO',
                     'TP_ESTACAO',
                     'VL_LATITUDE',
                     'CD_WSI',
                     'CD_DISTRITO',
                     'VL_ALTITUDE',
                     'SG_ESTADO',
                     'SG_ENTIDADE',
                     'CD_ESTACAO',
                     'VL_LONGITUDE',
                     'DT_INICIO_OPERACAO']
        
        api = InmetStation()
        stations = api.list_stations("M")
        col_names_stations = stations.columns.tolist()
        self.assertEqual(col_names_stations, col_names)
        
        
    def test_list_stations_wrong_input(self):
    
        api = InmetStation()
        self.assertRaises(ValueError, api.list_stations, "s")
        
        
    def test_get_all_stations(self):
        
        col_names = ['VEN_DIR',
                     'DT_MEDICAO',
                     'DC_NOME',
                     'CHUVA',
                     'PRE_INS',
                     'VL_LATITUDE',
                     'PRE_MIN',
                     'UMD_MAX',
                     'PRE_MAX',
                     'VEN_VEL',
                     'UF',
                     'PTO_MIN',
                     'TEM_MAX',
                     'RAD_GLO',
                     'PTO_INS',
                     'VEN_RAJ',
                     'TEM_INS',
                     'UMD_INS',
                     'CD_ESTACAO',
                     'TEM_MIN',
                     'VL_LONGITUDE',
                     'HR_MEDICAO',
                     'UMD_MIN',
                     'PTO_MAX']
        
        api = InmetStation()
        station_data = api.get_all_stations("2021-05-01")
        col_names_result = station_data.columns.tolist()
        self.assertEqual(col_names_result, col_names)
        
        
    
        
        
    
    


if __name__ == "__main__":
    unittest.main()