import requests 
import pandas as pd 
import datetime 
from typing import Optional, Union, List
from pandas.core.frame import DataFrame


class InmetStation:
    
    def __init__(self):
        self.api = "https://apitempo.inmet.gov.br"
        
    def _get_request(self,
            request:requests.models.Response,
            save_file=False,
            date=None,
            station_id=None,
            start_date=None,
            end_date=None) -> Union[DataFrame,int]:
        
        if request.status_code == 200:
            stations = request.json()
            df_stations = pd.json_normalize(stations)

            if save_file:
                if station_id:
                    print('date')
                    print('station_id')

                    df_stations.to_csv(f"inmet_data_{station_id}_{start_date}_{end_date}.csv", index=False)
                    print(f"file 'inmet_data_{station_id}_{start_date}_{end_date}.csv' was downloaded")
                if date:
                    print('date')
                    print('station_id')

                    df_stations.to_csv(f"inmet_data_{date}.csv", index=False)
                    print(f"file 'inmet_data_{date}.csv' was downloaded")
            else:
                return df_stations
        else:
            return request.status_code
        
    def _rename_vars_to_cf(self, df:DataFrame, by:str) -> DataFrame:
        """Rename original columns names to metric systems (https://dev.meteostat.net/formats.html#time-format)

        Parameters
        ----------
        df : DataFrame
            A pandas dataframe with the original columns names (in portuguese)
        by : str
            The time resolution of df. Different columns names for "hourly" and "daily".

        Returns
        -------
        DataFrame
            A pandas dataframe with renamed columns names.
        """        
        
        if by == "hour":
        
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
        
        elif by == "day":
            
            cols_daily_cf = {"DC_NOME": "STATION_NAME",
                              "VL_LATITUDE":"LAT",
                              "UF": "ST",
                              "TEM_MIN":"MIN_TEMP",
                              "VL_LONGITUDE":"LONG",
                              "UMID_MIN":"MIN_RH",
                              "DT_MEDICAO":"DATE",
                              "CHUVA":"RAIN",
                              "UMID_MED":"AVG_RH",
                              "VEL_VENTO_MED":"WSPD",
                              "TEM_MAX":"MAX_TEMP",
                              "CD_ESTACAO":"STATION_ID"}
            
            df.rename(columns = cols_daily_cf, inplace = True)
        
        return df
        
    def _check_date_format(self, date:str) -> bool:
        """Check user input date format.

        Parameters
        ----------
        date : str
            A date to check the format. 

        Returns
        -------
        bool
            If date format is valid, True is returned.

        Raises
        ------
        ValueError
            Wrong date format input.
        """        
        
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except:
            raise ValueError("Incorrect date format, date should be in 'YYYY-MM-DD' format.")
            
        
    def _check_data_station(self, df:DataFrame, by:str) -> bool:
        """Check if the queried data result is empty.

        Parameters
        ----------
        df : DataFrame
            The queried data.
        by : str
            The time resolution of the queried data.

        Returns
        -------
        bool
            If the queried result contains data from any station, returns True, False otherwise.
        """        
        
        if by == "hour":
            cols_filled = ["DC_NOME", "UF", "DT_MEDICAO","VL_LATITUDE", "VL_LONGITUDE", "CD_ESTACAO", "HR_MEDICAO"]
        
        elif by == "day":
            cols_filled = ["DC_NOME", "UF", "DT_MEDICAO","VL_LATITUDE", "VL_LONGITUDE", "CD_ESTACAO"]
        
        if any(df.drop(columns = cols_filled).count() != 0):
            return True 
        else:
            return False 
        
    def _create_date_time(self, df:DataFrame, by:str) -> DataFrame:
        
        if by == "hour":
            time_col = df["TIME"]
            date_col = df["DATE"]
            
            date_time_str = date_col + " " + time_col 
            date_time = pd.to_datetime(date_time_str,  format = "%Y-%m-%d %H%M")
            
            df.insert(0, "DATETIME", date_time)
            
            cols_drop = ["DATE","TIME"]
            df.drop(columns=cols_drop, inplace=True)
        
        elif by == "day":
            date_col = df["DATE"]
            date_dt = pd.to_datetime(date_col, format = "%Y-%m-%d")
            cols_drop = ["DATE"]
            df.drop(columns=cols_drop, inplace=True)
            
            df.insert(0,"DATE",date_dt)
            
        return df
    
    def _change_data_type(self, df:DataFrame, by:str) -> DataFrame:
        
        if by == "hour":
            to_int = ["MIN_RH","WDIR","MAX_RH","HUMI"]
            to_float = ["PRES","TEM_SEN","LAT","MAX_PRES","DWPT","MIN_TEMP",
                        "LONG","MAX_DWPT","RAIN","MIN_PRES","WSPD","MIN_DWPT",
                        "MAX_TEMP","WGST","TEMP"]
            
        elif by == "day":
            to_int = ["MIN_RH"]
            to_float = ["LAT","LONG","AVG_RH","TEMP_MED","RAIN","TEMP_MIN","TEMP_MAX",
                        "WSPD"]
            
        
        df[to_int] = df[to_int].apply(pd.to_numeric, errors="coerce").astype("Int64")
        df[to_float] = df[to_float].apply(pd.to_numeric, errors="coerce").astype("float64")
        df[["LAT","LONG"]] = round(df[["LAT","LONG"]], 5)
        
        return df
    
    def _count_date_diff(self, start_date:str, end_date:str) -> int:
        
        date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        total_days = (date_end - date_start).days
        
        return total_days
    
    def _split_dates(self, start_date:str, end_date:str, n_chunks:Optional[Union[str,int]]) -> int:
        
        total_days = self._count_date_diff(start_date, end_date)
        
        if n_chunks == "auto":
            return None
        
    def _is_state(self, st:List) -> None:
        """Check if input is a valid brazilian state abbreviation

        Parameters
        ----------
        st : List
            A list of brazilian states abbreviated.

        Raises
        ------
        ValueError
            Wrong abbreviation used.
        """        
        
        br_states = ["AC","AL","AP","AM","BA",
                     "CE","DF","ES","GO","MA",
                     "MT","MS","MG","PA","PB",
                     "PR","PE","PI","RJ","RN",
                     "RS","RO","RR","SC","SP",
                     "SE","TO"]
        
        for state in st:
            
            if state in br_states:
                pass
            else:
                raise ValueError(f"{state} is not a valid brazilian state abbreviation.")
            
        
    def list_stations(self, station_type:str, save_file=False) -> Union[DataFrame, str]:
        """List all stations available on INMET API.

        Parameters
        ----------
        station_type : str
            Station type. "T" for automatic station and "M" for manual stations.
        save_file : bool, optional
            Save output to csv file, by default False

        Returns
        -------
        Union[DataFrame, str]
            A pandas dataframe containing all stations.

        Raises
        ------
        ValueError
            Wrong input for station_type.
        """        
        
        if station_type not in ["T","M"]:
            raise ValueError('type must be either "T" (Automatic) or "M" (Manual)')
        else:
            r = requests.get("/".join([self.api, "estacoes", station_type]))
            if r.status_code == 200:
                stations = r.json()
                df_stations = pd.json_normalize(stations)
                
                if save_file:
                    df_stations.to_csv(f"inmet_stations_{station_type}.csv", index=False)
                    print(f"file 'inmet_stations_{station_type}.csv' was downloaded")
                else:
                    return df_stations
            else:
                return r.status_code
            
            
    def get_all_stations(self, date:str=None, save_file=False):

        if date == None:
            date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        
        self._check_date_format(date)
        
        r = requests.get("/".join([self.api, "estacao", "dados", date]))
        return self._get_request(r, save_file=save_file, date=date)
    
        
    def get_data_station(self, 
                         start_date:str,
                         end_date:str,
                         by:str,
                         station_id:Union[str,List[str]],
                         save_file:bool = False,
                         chunks:Optional[Union[str,int]] = None) -> DataFrame:
        
        self._check_date_format(start_date)
        self._check_date_format(end_date)
        
        if by == "hour":
            query = [self.api, "estacao", start_date, end_date]
        elif by == "day":
            query = [self.api, "estacao", "diaria", start_date, end_date]
        else:
            raise ValueError("by argument is missing")
    
        if isinstance(station_id, list):
            
            stations_df = pd.DataFrame()
            for station in station_id:
                print(station)
                print(f"Looking for station {station}...")
                
                query1 = query.copy()
                query1.append(station)
                r = requests.get("/".join(query1))
                
                if r.status_code == 200:
                    df_station = pd.json_normalize(r.json())
                    if self._check_data_station(df_station, by):
                        stations_df = stations_df.append(df_station)
                    else:
                        print(f"No data available for this period for station {station}")
                        
                elif r.status_code == 204:
                    print(f"There is no station {station}")
                    continue
                
                elif r.status_code == 403:
                    raise MemoryError("""The amount of data is too large for this request.
                                        Use the 'chunks' argument to split your request.""")
                    
                else:
                    print(f"Request error: Request status {r.status_code}")
                
            stations_df = self._rename_vars_to_cf(stations_df, by)
            stations_df = self._create_date_time(stations_df, by)
            stations_df = self._change_data_type(stations_df, by)
            stations_df.reset_index(inplace = True)
            
            if save_file:
                stations_df.to_csv(f"inmet_data_{start_date}_{end_date}.csv", index=False)
                print(f"file 'inmet_data_{start_date}_{end_date}.csv' was downloaded")
            else:
                return stations_df
                
        elif isinstance(station_id, str):
            
            r = requests.get("/".join([self.api, 
                            "estacao",
                            start_date,
                            end_date,
                            station_id]))
            
            return self._get_request(r, save_file=save_file, station_id=station_id, start_date=start_date, end_date=end_date)
            
        else:
            raise ValueError("station_id should be list or str.")
        
        
    def search_station_by_state(self, st:List) -> DataFrame:
        
        self._is_state(st)
        
        all_stations = self.list_stations()
        
        stations = all_stations[all_stations['SG_ESTADO'].isin(st)]
        
        return stations 
            
        
        
        
            
            
    
    
        
                
