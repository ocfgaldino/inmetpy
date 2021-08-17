import requests 
import pandas as pd 
import datetime 
from typing import Union, List
from pandas.core.frame import DataFrame


class InmetStation:
    
    def __init__(self):
        self.api = "https://apitempo.inmet.gov.br"
        
    def __get_request(self, request:requests.models.Response) -> Union[DataFrame,int]:
        
        if request.status_code == 200:
            stations = request.json()
            df_stations = pd.json_normalize(stations)
            return df_stations
        else:
            return request.status_code
        
    def __rename_vars_to_cf(df:DataFrame):
        
        cols_hourly_cf = {"DC_NOME": "station_name",
                          "PRE_INS": "",
                          "TEM_SEN": "",
                          "VL_LATITUDE":"latitude",
                          "PRE_MAX":"",
                          "UF": "ST",
                          "RAD_GLO":"",
                          "PTO_INS":"",
                          "TEM_MIN":"",
                          "VL_LONGITUDE":"longitude",
                          "UMD_MIN":"",
                          "PTO_MAX":"",
                          "VEN_DIR":"wind_direction",
                          "DT_MEDICAO":"",
                          "CHUVA":"",
                          "PRE_MIN":"",
                          "UMD_MAX":"",
                          "VEN_VEL":"wind_speed",
                          "PTO_MIN":"",
                          "TEM_MAX":"",
                          "VEN_RAJ":"wind_gust",
                          "TEM_INS":"",
                          "UMD_INS":"",
                          "CD_ESTACAO":"station_id",
                          "HR_MEDICA":"time"}
        
        cols_daily_cf = {"UMID_MED":"",
                         "DT_MEDICAO":"date",
                         "DC_NOME":"station_name"}
        
        
    def __check_date_format(self, date:str) -> bool:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            print("Incorrect date format, date should be in 'YYYY-MM-DD' format.")
            return False
        
    def __check_data_station(self, df:DataFrame) -> bool:
        
        
        
    def list_stations(self, type:str) -> Union[DataFrame, str]:
        
        if type not in ["T","M"]:
            raise ValueError('type must be either "T" (Automatic) or "M" (Manual)')
        else:
            r = requests.get("/".join([self.api, "estacoes", type]))
            if r.status_code == 200:
                stations = r.json()
                df_stations = pd.json_normalize(stations)
                
                return df_stations
            else:
                return r.status_code
            
            
    def get_all_stations(self, date:str):
        
        self.__check_date_format(date)
        
        r = requests.get("/".join([self.api, "estacao", "dados", date]))
        return self.__get_request(r)
    
        
    def get_station_data(self, start_date:str, end_date:str, station_id:Union[str,List[str]]) -> DataFrame:
        
        self.__check_date_format(start_date)
        self.__check_date_format(end_date)
        
        if isinstance(station_id, list):
            
            stations_df = pd.DataFrame()
            for station in station_id:
                print(f"Looking for station {station}...")
                
                r = requests.get("/".join([self.api, 
                            "estacao",
                            start_date,
                            end_date,
                            station_id]))
                
                if r.status_code == 200:
                    df_station = pd.json_normalize(r.json())
                    stations_df = pd.append(stations_df, df_station)
                elif r.status_code == 204:
                    print(f"No data for station {station}")
                    
                    continue
                
                
        

        
        
        return self.__get_request(r)
    
    
        
                