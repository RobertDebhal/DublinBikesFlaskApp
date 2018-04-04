import json
import requests
import pandas as pd
import sqlalchemy
from time import sleep, time
# import traceback
# import logging
import smtplib
# from sqlalchemy.sql.schema import Table
import updateStaticData

# source https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
api_token = '7e813fe2e25367cd1aa3c4403c764332448fce48' 
api_url_base = 'https://api.jcdecaux.com/vls/v1/'

def get_contracts_info():
    """
    Function to retrieve static and dynamic (real time) data 
    for DublinBikes in JSON format.
    """
    #response = requests.get(api_url, headers=headers)
    response = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}'.format(api_token))

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_weather_info():
    """
    Function to retrieve static and dynamic (real time) data 
    for Dublin WEather in JSON format.
    """
    #response = requests.get(api_url, headers=headers)
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&APPID=70ef396e3ce3949e0934b4428e41f453')

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
def main():
    #if doesn't exist make table
    
    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    conn = engine.connect()
    while True:
        try:
            check=get_weather_info()
        except requests.exception.ConnectionError:
            sleep(600)
            continue
        try:
            dublin_stations_test = get_contracts_info()
        except requests.exception.ConnectionError:
            sleep(600)
            continue
        #need to compare df(contains dynamic bike info to be saved) 
        #to static station list to check for new stations 
        for i in range(len(dublin_stations_test)):
            dublin_stations_test[i]['latest_weather']=check['dt']
            
        static = ['contract_name','name','address','position','banking','bonus']
         
        #converting json to data frame
        df = pd.read_json(json.dumps(dublin_stations_test))
        
        df_query_static_numbers=pd.read_sql_query('SELECT number from static', engine)
        if df.shape[0]>df_query_static_numbers.shape[0]:
            updateStaticData.update_static(dublin_stations_test, engine, conn)
            
        for i in static:
            df.drop(i,1, inplace = True)
        
        df_weather = pd.DataFrame({'date':[check['dt']],'temperature':[round(float(check['main']['temp'])-273.15,2)],
                                   'conditions':[check['weather'][0]['main']],'description':check['weather'][0]['description'],
                                   'wind':[check['wind']['speed']],'clouds':[check['clouds']['all']],
                                   'sunrise':[check['sys']['sunrise']],'sunset':[check['sys']['sunset']]})
     
     
        #appending data frame to SQL table in RDS
        try:
            df.to_sql(name='dynamic',con=conn,if_exists='append',index=False)
        except sqlalchemy.exc.IntegrityError:
            pass
        try:
            df_weather.to_sql(name='weather',con=conn,if_exists='append',index=False)
        except sqlalchemy.exc.IntegrityError:
            pass
# #         df1 = pd.read_sql_query('SELECT number, available_bikes FROM stations', engine)
# #         print(df1)
        #openweather cut us off requesting every 5 minutes
        with open('check_file','w') as file:
            file.write(str(time()))
        sleep(600)

if __name__=='__main__':
    main()
