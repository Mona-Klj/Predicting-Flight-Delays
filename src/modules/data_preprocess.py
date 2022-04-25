import numpy as np
import pandas as pd

def preprocess(df):
    """
    Conduct data cleaning and feature engineering for flight delay prediction.
    PARAMS:
        df (pd.DataFrame): dataframe containing raw data
    RETURNS:
        data (pd.DataFrame): preprocessed data
    """
    # make a copy to keep original df unchanged.
    data = df.copy()
    
    # some columns are in flights file but not in test file
    #_____________________________________________________
    
    # decide if it's flights data or flights_test data
    if data.shape[1] > 20:
        # operations for flights file only
        data.drop(columns='no_name', inplace=True)
        # drop rows with NaN in 'arr_delay' since it's target variable 
        data.dropna(subset=['arr_delay'], inplace=True)
        data.fillna({'first_dep_time': 'no first dep',
                   'longest_add_gtime': 0,
                   'total_add_gtime': 0,
                   'cancellation_code': 'not cancelled',
                   'late_aircraft_delay': 0,
                   'security_delay': 0,
                   'nas_delay': 0,
                   'weather_delay': 0,
                   'carrier_delay': 0,
                   'dep_delay': 0},
                  inplace=True)
    

    # feature engineering, operations for both data files
    #_____________________________________________________

    # drop columns containing repeated or useless information
    data.drop(columns=['mkt_carrier',
                     'branded_code_share',
                     'mkt_carrier_fl_num',
                     'origin',
                     'dest',
                     'dup',
                     'flights'],
            inplace=True)
    
    # create a column suggesting if carriers share code is shared, then drop 'mkt_unique_carrier'
    data['share_code'] = (data['mkt_unique_carrier'] != data['op_unique_carrier']).astype('int')
    data.drop(columns='mkt_unique_carrier', inplace=True)
    
    # Columns about origin and destination
    #_____________________________________________________
    
    # split city and states in 'origin_city_name' & 'dest_city_name' columns and drop them afterwards 
    data[['origin_city', 'origin_state']] = data['origin_city_name'].str.split(',', expand=True, n=2)
    data[['dest_city', 'dest_state']] = data['dest_city_name'].str.split(',', expand=True, n=2)
    data.drop(columns=['origin_city_name', 'dest_city_name'], inplace=True)
       
    # Columns about time
    #_____________________________________________________
    
    # convert datetime columns into pd.datetime for following extraction & calculation use
    data['fl_date'] = pd.to_datetime(data['fl_date'])
    data['crs_dep_time'] = pd.to_datetime(data['crs_dep_time'].astype(str).str.zfill(4),
                                          format='%H%M', 
                                          errors='coerce')
    data['crs_arr_time'] = pd.to_datetime(data['crs_arr_time'].astype(str).str.zfill(4),
                                          format='%H%M',
                                          errors='coerce')

    
    # add arrival date
    # flights data +1 for the flights arrive on next day
    data['arr_date'] = pd.to_datetime(np.where(data['crs_dep_time'] > data['crs_arr_time'],
                                               (data['fl_date'] + pd.to_timedelta(1, unit='D')).dt.date,
                                               data['fl_date'].dt.date))
    data.dropna(subset=['crs_dep_time', 'crs_arr_time', 'fl_date', 'arr_date'], inplace=True)
    # for departure and arrival, each merge date and time into one column
    data['dep_datetime'] = pd.to_datetime(data['fl_date'].astype(str) + ' ' + data['crs_dep_time'].astype(str))
    data['arr_datetime'] = pd.to_datetime(data['arr_date'].astype(str) + ' ' + data['crs_arr_time'].astype(str))
    
    # extract month and day of the week from flight date
    data['fl_month'] = data.fl_date.dt.month
    data['fl_weekday'] = data.fl_date.dt.dayofweek
    data['season'] = data.fl_month % 12 // 3 + 1
    
    # convert departure and arrival time to minutes of the day
    data['dep_min_of_day'] = (data['dep_datetime'].dt.hour) * 60 + (data['dep_datetime'].dt.minute)
    data['arr_min_of_day'] = (data['arr_datetime'].dt.hour) * 60 + (data['arr_datetime'].dt.minute)
    
    # extract departure and arrival hour
    data['dep_hr'] = data['dep_datetime'].dt.hour
    data['arr_hr'] = data['arr_datetime'].dt.hour
    
    # make departure time columns circular by convert with sin and cos
    data['dep_min_sin'] = np.sin(data.dep_min_of_day * (2. * np.pi / 1440)) # divided by total minutes in a day
    data['dep_min_cos'] = np.cos(data.dep_min_of_day * (2. * np.pi / 1440))
    data['dep_hr_sin'] = np.sin(data.dep_hr * (2. * np.pi / 24)) # divided by total number of hours
    data['dep_hr_cos'] = np.cos(data.dep_hr * (2. * np.pi / 24))
    data['arr_min_sin'] = np.sin(data.arr_min_of_day * (2. * np.pi / 1440)) # divided by total minutes in a day
    data['arr_min_cos'] = np.cos(data.arr_min_of_day * (2. * np.pi / 1440))
    data['arr_hr_sin'] = np.sin(data.arr_hr * (2. * np.pi / 24))
    data['arr_hr_cos'] = np.cos(data.arr_hr * (2. * np.pi / 24))
    data['fl_mnth_sin'] = np.sin(data.fl_month * (2. * np.pi / 12)) # divided by total number of months
    data['fl_mnth_cos'] = np.cos(data.fl_month * (2. * np.pi / 12))
    data['fl_wkday_sin'] = np.sin(data.fl_weekday * (2. * np.pi / 7)) # divided by number of days in a week
    data['fl_wkday_cos'] = np.cos(data.fl_weekday * (2. * np.pi / 7)) 
    
        
    # calculate number of flights scheduled for departure at each airport each day
    num_of_flights = data[['fl_date', 'origin_airport_id', 'op_carrier_fl_num']].groupby(['fl_date', 'origin_airport_id'], as_index=False).count().rename(columns={'op_carrier_fl_num': 'day_num_of_flights'})
    data = pd.merge(data, num_of_flights, on=['fl_date', 'origin_airport_id'], how='left')
    
    # add a column to determine if it is busy around its departure time (6 hrs in the middle)
    # for each flight, time frame is in between 3 hrs earlier and 3 hrs later of its departure time at same airport
    # calculate total number of flights scheduled for departure and arrival in that timeframe
    num_dep = data.apply(lambda x: data[data['origin_airport_id']==x['origin_airport_id']]['dep_datetime'].between((x['dep_datetime'] - pd.to_timedelta(3, unit='H')), (x['dep_datetime'] + pd.to_timedelta(3, unit='H'))).sum(), axis=1)
    num_arr = data.apply(lambda x: data[data['dest_airport_id']==x['origin_airport_id']]['arr_datetime'].between((x['dep_datetime'] - pd.to_timedelta(3, unit='H')), (x['dep_datetime'] + pd.to_timedelta(3, unit='H'))).sum(), axis=1)
    data['num_flights_6hrs'] = num_dep + num_arr
    
    # add a column suggesting number of flights with same plane (inbound flight) within 2 hrs ahead of each flight's departure
    data['inbound_fl_num'] = data.apply(lambda x: (data[(data['tail_num']==x['tail_num']) & (data['arr_datetime'].between(x['dep_datetime']-pd.to_timedelta(2, unit='H'), x['dep_datetime']))]['tail_num'].count()), axis=1 )
    data['inbound_fl'] = (data['inbound_fl_num'] > 0).astype(int)
    
    return data    
    
    
    






