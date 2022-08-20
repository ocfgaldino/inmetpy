import requests
import pandas as pd
import datetime
from typing import Optional, Union, List
from pandas.core.frame import DataFrame
import math
import numpy as np
from yaspin import yaspin
from exceptions import RequestTooLarge



class InmetStation:

    def __init__(self):
        self._api = "https://apitempo.inmet.gov.br"
        self.stations = self._get_all_stations()
        self._is_capital()
        self._change_data_type_station_details()

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
            df_stations = self._rename_vars_to_cf(df_stations, 'hour')

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
    
    def _rename_cols_to_en(self, df:DataFrame) -> DataFrame:
        """Rename original columns names from portuguese to english

        Parameters
        ----------
        df : DataFrame
            A pandas dataframe with the original columns names (in portuguese)

        Returns
        -------
        DataFrame
            A pandas dataframe with renamed columns names.
        """
        
        cols_to_en = {
                    "DC_NOME": "STATION_NAME",
                    "DT_FIM_OPERACAO":"END_DATE_OPERATION",
                    "FL_CAPITAL":"IS_CAPITAL",
                    "CD_SITUACAO":"CD_SITUATION",
                    "TP_ESTACAO":"TP_STATION",
                    "SG_ESTADO":"STATE",
                    "VL_LATITUDE":"LATITUDE",
                    "VL_LONGITUDE":"LONGITUDE",
                    "VL_ALTITUDE":"HEIGHT",
                    "DT_INICIO_OPERACAO":"START_DATE_OPERATION",
                    "SG_ENTIDADE":"INSTITUTE",
                    "CD_DISTRITO":"CD_DISTRICT",
                    "CD_ESTACAO":"CD_STATION"
                    }
        
        
        
        df.rename(columns = cols_to_en, inplace = True)
        
        df.loc[df['TP_STATION']=="Automatica", "TP_STATION"] = "Automatic"
        df.loc[df['TP_STATION']=="Convencional", "TP_STATION"] = "Traditional"
       
        df.loc[df['CD_SITUATION']=="Operante", "CD_SITUATION"] = "Operative"
        df.loc[df['CD_SITUATION']=="Pane", "CD_SITUATION"] = "Down"
        
        
        return df
        
    def _is_capital(self) -> DataFrame:
        """Change 'IS_CAPITAL' column from string to boolen"""
        self.stations['IS_CAPITAL'] = self.stations['IS_CAPITAL'].apply(lambda x: True if x == 'S' else False)

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
        """Create a datetime column in the queried data.

        Parameters
        ----------
        df : DataFrame
            The queried data.
        by : str
            The time resolution. By "hour" or "day".

        Returns
        -------
        DataFrame
            The original dataframe with one more column. A datetime column.
        """

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
        """Change the data type of each attribute of the queried data.

        Parameters
        ----------
        df : DataFrame
            The queried data.
        by : str
            The time resolution of the queried data.

        Returns
        -------
        DataFrame
            The original dataframe with the correct data types format for each attribute.
        """

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

    def _change_data_type_station_details(self) -> DataFrame:

        to_float = ['HEIGHT','LATITUDE','LONGITUDE']
        to_date_time = ['END_DATE_OPERATION', 'START_DATE_OPERATION']

        self.stations[to_float] = self.stations[to_float].apply(pd.to_numeric, errors='coerce').astype("float64")
        self.stations[to_date_time] = self.stations[to_date_time].apply(pd.to_datetime, format="%Y-%m-%d", utc=True, errors='coerce')


    def _count_date_diff(self, start_date:str, end_date:str) -> int:
        """Count the total of days queried.

        Parameters
        ----------
        start_date : str
            The query start date.
        end_date : str
            The query end date.

        Returns
        -------
        int
            The total of days queried.
        """

        date_start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        date_end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        total_days = (date_end - date_start).days

        return total_days

    def _split_dates(self, start_date:str, end_date:str) -> int:
        """Generate a dictionary with 'start_date's and 'end_date's.
        Used when 'chunk' argument is set to 'True'. Divide a long period into
        smaller periods, of 1 year maximum.

        Parameters
        ----------
        start_date : str
            The first date for the whole period.
        end_date : str
            The last date for the whole period.

        Returns
        -------
        dict
            A dictionary containing pair of dates.
        """
        total_days = self._count_date_diff(start_date, end_date)

        first_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        max_days = 366

        if total_days < max_days:
            return None

        else:
            total_chunks = math.ceil(total_days/max_days)

            days_end = list()
            days_diff = max_days

            list_dates = {'start_date':[],'end_date':[]}
            add_day = 0

            for n in range(total_chunks):

                if n + 1 == total_chunks:
                    days_diff = total_days % max_days

                if n != 0:
                    add_day = 1

                days_start = n * max_days
                days_end = days_start + days_diff

                start_date = first_date + datetime.timedelta(days=days_start + add_day)
                end_date = first_date + datetime.timedelta(days=days_end)

                start_date_str = datetime.datetime.strftime(start_date, "%Y-%m-%d")
                end_date_str = datetime.datetime.strftime(end_date, "%Y-%m-%d")

                list_dates["start_date"].append(start_date_str)
                list_dates["end_date"].append(end_date_str)

            return list_dates

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

    def _haversine(self,
                   lat_1:float,
                   lon_1:float,
                   lat_2:float,
                   lon_2:float) -> float:
        """Calculate distance between two points using the Haversine Formula.
        (https://en.wikipedia.org/wiki/Haversine_formula)

        Parameters
        ----------
        lat_1 : float
            Latitude for point 1.
        lon_1 : float
            Longitude for point 1.
        lat_2 : float
            Latitudade for point 2.
        lon_2 : float
            Longitude for point 2.

        Returns
        -------
        float
            The distance, in kilometers, between the two coordinates.
        """

        lon_1, lat_1, lon_2, lat_2 = map(math.radians, [lon_1, lat_1, lon_2, lat_2])
        dlon = lon_2 - lon_1
        dlat = lat_2 - lat_1

        hav = np.sin(dlat/2)**2 + np.cos(lat_1) * np.cos(lat_2) * np.sin(dlon/2)**2

        d = 2 * np.arcsin(np.sqrt(hav))

        earth_radius_km = 6371

        km = earth_radius_km * d

        return km


    def _get_stations_details(self, type):
        """Get details of automatic OR manual stations available on INMET API.

        Returns
        -------
        DataFrame
            A pandas dataframe containing details of the stations.
        """
        
        if type == "A":
            type = "T"
        
        r = requests.get("/".join([self._api, "estacoes", type]))
        if r.status_code == 200:
            stations = r.json()
            df_stations = pd.json_normalize(stations)
            
            return self._rename_cols_to_en(df_stations)
        else:
            raise ConnectionError(f"API error code: {r.status_code}")
            
        
    def _get_all_stations(self):
        """Get details of all stations available on INMET API.

        Returns
        -------
        DataFrame
            A pandas dataframe containing details of all stations.
        """

        df_automatic_stations = self._get_stations_details("A")
        df_manual_stations = self._get_stations_details("M")
        
        stations = pd.concat([df_automatic_stations, df_manual_stations])
        stations.reset_index(inplace=True, drop=True)

        return stations

    def _check_is_station(self, stations:list) -> None:
        """Check if station list input has only valid stations

        Parameters
        ----------
        stations : List
            A list of stations.

        Raises
        ------
        ValueError
            Wrong station code.
        """

        unexist_stations = list(set(stations) - set(self.stations['CD_STATION']))

        if unexist_stations:
            raise ValueError("There is no station(s): " + ", ".join(f'"{station}"' for station in unexist_stations))
        else:
            pass
            
    def _check_station_type(self, station_type):
        """Check if input for station_type is valid.

        Parameters
        ----------
        station_type : str
            Type of station.

        Raises
        ------
        ValueError
            Wrong station type.
        """

        if station_type not in ["A","M", "ALL"]:
            raise ValueError('station_type must be either "A" (Automatic), "M" (Manual) or "ALL" (All stations)"')
        else:
            pass

    def _check_request_size(self, start_date, end_date):
        """Check the size of requested data

        Parameters
        ----------
        start_date : str
            Start date for search.
        end_date: str
            End date for search.

        Raises
        ------
        RequestTooLarge
            Requested data greater than one year period.
        """

        date_format = "%Y-%m-%d"

        if (datetime.datetime.strptime(end_date, date_format) - datetime.datetime.strptime(start_date, date_format)).days > 366:
            raise RequestTooLarge("""The maximum interval is 1 year between start_date and end_date. Use 'chunks=True' to split your request""")
        else:
            pass


    def get_manual_stations(self)  -> DataFrame:
        """Get a list of detailhs of all traditional/manual stations.

        Returns
        -------
        DataFrame
            A pandas dataframe containing details of all manual stations.
        """

        stations = self.stations 
        return stations[stations['TP_STATION']=='Traditional']

    def get_auto_stations(self) -> DataFrame:
        """Get a list of detailhs of all automatic stations.

        Returns
        -------
        DataFrame
            A pandas dataframe containing details of all automatic stations.
        """

        stations = self.stations 
        return stations[stations['TP_STATION']=='Automatic']


    def get_all_stations(self, date:str=None, save_file=False) -> DataFrame:
        """Get data from all stations at given date at "date".

        Parameters
        ----------
        date : str
            Date to query data.
        Returns
        -------
        DataFrame
            A pandas dataframe with data from all stations available at given date.
        """

        if date == None:
            date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")

        self._check_date_format(date)

        r = requests.get("/".join([self._api, "estacao", "dados", date]))

        return self._get_request(r, save_file=save_file, date=date)


    def get_data_station(self,
                         start_date:str,
                         end_date:str,
                         by:str,
                         station_id:List[str],
                         save_file:bool = False,
                         chunks:Optional[bool] = False) -> DataFrame:
        """Get data from all stations in 'stations_id'. The data can be downloaded
        either by 'hour' or 'day'. In case a long period is request, the 'chunks'
        argument can be set to True (default is False).

        Returns
        -------
        DataFrame
            A dataframe containing the data for the whole period and all stations
            requested.

        Raises
        ------
        ValueError
            The 'by' argument should be 'hour' or 'day'.
        TypeError
            The 'station_id' should be a list.
        """

        self._check_date_format(start_date)
        self._check_date_format(end_date)
        self._check_is_station(station_id)
                

        if chunks == False:
            self._check_request_size(start_date, end_date)
            dates = {'start_date':[start_date], 'end_date':[end_date]}
        else:
            dates = self._split_dates(start_date, end_date)

        start_date_list = dates['start_date']
        end_date_list = dates['end_date']

        if by == "hour":
            base_query = [self._api, "estacao"]
        elif by == "day":
            base_query = [self._api, "estacao", "diaria"]
        else:
            raise ValueError("by argument is missing") 


        if isinstance(station_id, list):

            stations_df = pd.DataFrame()

            for period in range(len(start_date_list)):

                start_date = start_date_list[period]
                end_date = end_date_list[period]

                for station in station_id:
                    print(f"Requesting data for station {station} from {start_date} to {end_date}.")
                    
                    full_query = base_query.copy()                            
                    full_query.extend([start_date, end_date, station])
                    with yaspin(text="Requesting data...", color="yellow") as spinner:
                        r = requests.get("/".join(full_query))

                        if r.status_code == 200:
                            df_station = pd.json_normalize(r.json())
                            with yaspin(text=f"Requesting data from station {station} from {start_date} to {end_date}.",
                                         color="cyan") as sp:
                                if self._check_data_station(df_station, by):
                                    stations_df = pd.concat([stations_df, df_station])
                                    sp.write("✔ Data available.")
                                    print("="*63)
                                else:
                                    sp.write(f"✕ No data available")
                                    print("="*63)
                                    continue
                        else:
                            print(f"Request error: Request status {r.status_code}")

            stations_df = self._rename_vars_to_cf(stations_df, by)
            stations_df = self._create_date_time(stations_df, by)
            stations_df = self._change_data_type(stations_df, by)
            stations_df.reset_index(inplace = True, drop=True)

            if save_file:
                stations_df.to_csv(f"inmet_data_{start_date}_{end_date}.csv", index=False)
                print(f"file 'inmet_data_{start_date}_{end_date}.csv' was downloaded")
            else:
                return stations_df

        else:
            raise TypeError("station_id should be list.")


    def search_station_by_state(self, 
                                st:List, 
                                station_type:str="ALL") -> DataFrame:
        """Search available stations for specific states.

        Parameters
        ----------
        st : List
            A list with the brazilian states searched (abbreviated).
        station_type : Type of station searched. "A" for automatic, "M" for manual
        and "ALL" for both types. Default is "ALL".

        Returns
        -------
        DataFrame
            A pandas dataframe with all stations available in the searched states.
        """

        self._is_state(st)
        self._check_station_type(station_type)

        if station_type == "A":
            stations = self.get_auto_stations()
        elif station_type == "M":
            stations = self.get_manual_stations()
        else:
            stations = self.stations

        stations = stations[stations['STATE'].isin(st)]

        return stations


    def search_station_by_coords(self,
                                 lat:float,
                                 lon:float,
                                 station_type:str="ALL",
                                 n_stations:int = 1) -> DataFrame:
        """Search the closest 'n' stations for a given coordinate.

        Parameters
        ----------
        lat : float
            The latitude of point searched.
        lon : float
            The longitude of point searched.
        station_type : Type of station searched. "A" for automatic, "M" for manual
        and "ALL" for both types. Default is "ALL".
        n_stations : int
            The number of stations to return. Default is 1.

        Returns
        -------
        DataFrame
            A pandas dataframe with details of the closest 'n' stations for
            the given coordinates.
        """
        if type(lat) != float or type(lon) != float:
            raise TypeError("Coordinates (lat,lon) values must be type 'float'")

        self._check_station_type(station_type)

        if station_type == "A":
            stations = self.get_auto_stations()
        elif station_type == "M":
            stations = self.get_manual_stations()
        else:
            stations = self.stations

        distance = []
        for _, row in stations.iterrows():           
            distance.append(self._haversine(float(row['LATITUDE']), float(row['LONGITUDE']), lat, lon))

        stations['DISTANCE'] = distance

        return stations.sort_values(by='DISTANCE').iloc[0:n_stations]
