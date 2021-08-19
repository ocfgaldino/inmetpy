import requests 
import pandas as pd 
import datetime 
from typing import Optional, Union, List
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
        
    def __rename_hourly_vars_to_cf(self, df:DataFrame) -> DataFrame:
        
        cols_hourly_cf = {"DC_NOME": "STATION_NAME",
                          "PRE_INS": "PRES",
                          "TEM_SEN": "TEM_SEN",
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
        
        df.rename(columns = cols_hourly_cf, inplace = True)
        
        return df
        
        
    def __rename_daily_vars_to_cf(self, df:DataFrame) -> DataFrame:
    
        cols_daily_cf = {"UMID_MED":"",
                        "DT_MEDICAO":"date",
                        "DC_NOME":"station_name"}
        
        df.columns = cols_daily_cf 
        
        return df
        
        
    def __check_date_format(self, date:str) -> bool:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            print("Incorrect date format, date should be in 'YYYY-MM-DD' format.")
            return False
        
    def __check_data_station_hr(self, df:DataFrame) -> bool:
        
        cols_filled = ["DC_NOME", "UF", "DT_MEDICAO","VL_LATITUDE", "VL_LONGITUDE", "CD_ESTACAO", "HR_MEDICAO"]
        
        if any(df.drop(columns = cols_filled).count() != 0):
            return True # has data
        else:
            return False # no data for this period
        
    def __create_date_time(self, df:DataFrame) -> DataFrame:
        
        time_col = df["TIME"]
        date_col = df["DATE"]
        
        date_time_str = date_col + " " + time_col 
        date_time = pd.to_datetime(date_time_str,  format = "%Y-%m-%d %H%M")
        
        df.insert(0, "date_time", date_time)
        
        cols_drop = ["DATE","TIME"]
        df.drop(columns=cols_drop, inplace=True)
        
        return df
    
    def __change_data_type(df:DataFrame) -> DataFrame:
        
        to_int = ["MIN_RH","WDIR","MAX_RH","HUMI"]
        to_float = ["PRES","TEM_SEN","LAT","MAX_PRES","DWPT","MIN_TEMP",
                    "LONG","MAX_DWPT","RAIN","MIN_PRES","WSPD","MIN_DWPT",
                    "MAX_TEMP","WGST","TEMP"]
        
        df[to_int] = df[to_int].astype("int64")
        df[to_float] = df[to_float].astype("float64")
        
        df[["LAT","LONG"]] = round(df[["LAT","LONG"]], 5)
        
        return df
    
    def __count_date_diff(self, start_date:str, end_date:str) -> int:
        
        date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        total_days = (date_end - date_start).days
        
        return total_days
    
    def __split_dates(self, start_date:str, end_date:str, n_chunks:Optional[Union[str,int]]) -> int:
        
        total_days = self.__count_date_diff(start_date, end_date)
        
        if n_chunks == "auto":
            return None
            
        
        
        
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
    
        
    def get_data_station_by_hour(self, 
                                 start_date:str, 
                                 end_date:str, 
                                 station_id:Union[str,List[str]],
                                 chunks:Optional[Union[str,int]] = None) -> DataFrame:
        
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
                            station]))
                
                if r.status_code == 200:
                    df_station = pd.json_normalize(r.json())
                    if self.__check_data_station_hr(df_station):
                        stations_df = stations_df.append(df_station)
                    else:
                        print(f"No data available for this period for station {station}")
                        
                elif r.status_code == 204:
                    print(f"There is no station {station}")
                    continue
                
            stations_df = self.__rename_hourly_vars_to_cf(stations_df)
            stations_df = self.__create_date_time(stations_df)
            stations_df.reset_index(inplace = True)
            
            return stations_df
                
        elif isinstance(station_id, str):
            
            r = requests.get("/".join([self.api, 
                        "estacao",
                        start_date,
                        end_date,
                        station_id]))
            
            return self.__get_request(r)
            
        else:
            raise ValueError("station_id shoud be list or str.")
            
            
                
                
    
    
        
                