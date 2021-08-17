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
        
        cols_hourly_cf = {"DC_NOME": "STATION_NAME",
                          "PRE_INS": "PRES",
                          "TEM_SEN": "",
                          "VL_LATITUDE":"LAT",
                          "PRE_MAX":"MAX_PRES",
                          "UF": "ST",
                          "RAD_GLO":"GLO_RAD",
                          "PTO_INS":"DWPT",
                          "TEM_MIN":"MIN_TEMP",
                          "VL_LONGITUDE":"LONG",
                          "UMD_MIN":"MIN_RH",
                          "PTO_MAX":"MAX_DWPT",
                          "VEN_DIR":"WDIR",
                          "DT_MEDICAO":"DATE",
                          "CHUVA":"RAIN",
                          "PRE_MIN":"MIN_PRES",
                          "UMD_MAX":"MAX_RH",
                          "VEN_VEL":"WSPD",
                          "PTO_MIN":"MIN_DWPT",
                          "TEM_MAX":"MAX_TEMP",
                          "VEN_RAJ":"WGST",
                          "TEM_INS":"TEMP",
                          "UMD_INS":"HUMI",
                          "CD_ESTACAO":"STATION_ID",
                          "HR_MEDICAO":"TIME"}
        
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
        
    #def __check_data_station(self, df:DataFrame) -> bool:
        
        
        
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
    
    
        
                