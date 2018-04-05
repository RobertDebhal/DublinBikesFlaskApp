import json
import requests
import pandas as pd
import sqlalchemy
from time import sleep, time
import sqlite3
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
    for Dublin Weather in JSON format.
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
	#creating local sqlite connection/database for quicker response to marker click queries
	enginesqlite = sqlite3.connect('most_recent_station_data.db')

    while True:
        try:
            check=get_weather_info()
        except requests.exception.ConnectionError as e:
			#writing error message without terminating script
			with open('logger','a') as file:
				file.write(e,"Time of error: "+str(time()))
            sleep(600)
            continue
        try:
            dublin_stations_test = get_contracts_info()
        except requests.exception.ConnectionError as e:
			#writing error message without terminating script
			with open('logger','a') as file:
				file.write(e, "Time of error: "+str(time()))
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
        except sqlalchemy.exc.IntegrityError as e:
			#writing error message without terminating script
			with open('logger','a') as file:
				file.write(e, "Time of error: "+str(time()))
        try:
            df_weather.to_sql(name='weather',con=conn,if_exists='append',index=False)
        except sqlalchemy.exc.IntegrityError as e:
			#writing error message without terminating script
			with open('logger','a') as file:
				file.write(e, "Time of error: "+str(time()))
		#saves latest time to file to easily check time of latest update locally, if desired
        with open('check_file','w') as file:
            file.write(str(time()))
        #openweather cut us off requesting every 5 minutes
		sleep(600)
		
		#Updating 'most_recent_station_data.db' with latest station info
		try:
		    most_recent_station_data_df = pd.read_sql_query('SELECT * FROM SE_group_project.dynamic, SE_group_project.static WHERE \
		    SE_group_project.dynamic.number=SE_group_project.static.number and (dynamic.number,last_update) in (SELECT dynamic.number, max(last_update)from \
		    SE_group_project.dynamic group by SE_group_project.dynamic.number);')
			
		    most_recent_station_data_df.to_sql(name = 'occupancy', con = enginesqlite, if_exists='replace',index=False, flavor='sqlite')
		except Exception as e:
			with open('logger','a') as file:
				file.write(e, "Time of error: "+str(time()))
			
			
if __name__=='__main__':
    main()
