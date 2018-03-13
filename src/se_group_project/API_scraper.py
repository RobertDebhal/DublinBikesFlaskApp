import json
import requests
import pandas as pd
import sqlalchemy
from time import sleep

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
    
engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()
while True:
    dublin_stations_test = get_contracts_info()
    
    #chaging positions filed to two separate lat and lng methods
    for i in range(len(dublin_stations_test)):
        dublin_stations_test[i]['lat']=dublin_stations_test[i]['position']['lat']
        dublin_stations_test[i]['lng']=dublin_stations_test[i]['position']['lng']

    for i in range(len(dublin_stations_test)):
        del(dublin_stations_test[i]['position'])
    
    #converting json to data frame
    df = pd.read_json(json.dumps(dublin_stations_test))
    
    #appending data frame to SQL table in RDS
    df.to_sql(name='dynamic',con=conn,if_exists='replace',index=False)

    df1 = pd.read_sql_query('SELECT name, lat, lng, available_bikes FROM stations WHERE name="BLACKHALL PLACE"', engine)
    print(df1)
    sleep(300)

