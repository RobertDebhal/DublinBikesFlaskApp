import json
import requests
import pandas as pd
import sqlalchemy
    


def update_static(dublin_stations_test, engine, conn):
    dynamic2 = ['status','bike_stands','available_bike_stands','available_bikes','last_update']

    #chaging positions filed to two separate lat and lng methods
    for i in range(len(dublin_stations_test)):
        dublin_stations_test[i]['lat']=dublin_stations_test[i]['position']['lat']
        dublin_stations_test[i]['lng']=dublin_stations_test[i]['position']['lng']
        
    for i in range(len(dublin_stations_test)):
        del(dublin_stations_test[i]['position'])
        
    df = pd.read_json(json.dumps(dublin_stations_test))
    for i in dynamic2:
        df.drop(i,1, inplace = True)
        
    df_query = pd.read_sql_query('SELECT * FROM static ORDER BY number desc', engine)
    print(df_query.shape)
    
    df_concat=pd.concat([df,df_query])
    
    df_concat_drop_duplicates=df_concat.drop_duplicates(subset='number',keep=False)
    
    df_concat_drop_duplicates.to_sql(name='static',con=conn,if_exists='append',index=False)

def main():
    from API_scraper import api_token, api_url_base, get_contracts_info

    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    conn = engine.connect()
    
    dublin_stations_test = get_contracts_info()
    
    update_static(dublin_stations_test, engine, conn)




if __name__ == "__main__":
    main()