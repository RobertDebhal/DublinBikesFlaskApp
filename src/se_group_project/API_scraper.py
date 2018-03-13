import json
import requests
import pandas as pd
import sqlalchemy

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
    
dublin_stations_test = get_contracts_info()

engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()

#converting json to data frame
df = pd.read_json(json.dumps(dublin_stations_test))
df.drop('position',1,inplace=True)

#appending data frame to SQL table in RDS
df.to_sql(name='stations',con=conn,if_exists='append')

df1 = pd.read_sql_query('SELECT name, available_bikes FROM stations', engine)
print(df1)

