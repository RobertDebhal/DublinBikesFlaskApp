import json
import requests
import pandas as pd
import sqlalchemy
from time import sleep
import datetime

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


    



def main():
    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    conn = engine.connect()
    while True:
        dublin_stations_test = get_contracts_info()
        for i in range(len(dublin_stations_test)):
            dublin_stations_test[i]['last_update']=datetime.datetime.fromtimestamp((int(dublin_stations_test[i]['last_update'])/1000)).strftime('%Y-%m-%d %H:%M:%S')
        
        static = ['contract_name','name','address','position','banking','bonus']
         
        #converting json to data frame
        df = pd.read_json(json.dumps(dublin_stations_test))
        for i in static:
            df.drop(i,1, inplace = True)
     
        #appending data frame to SQL table in RDS
        try:
            df.to_sql(name='dynamic',con=conn,if_exists='append',index=False)
        except sqlalchemy.exc.IntegrityError:
            pass 
#         df1 = pd.read_sql_query('SELECT number, available_bikes FROM stations', engine)
#         print(df1)
        sleep(300)

if __name__=='__main__':
    main()

