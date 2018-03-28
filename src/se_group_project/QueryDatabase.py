import json
import requests
import pandas as pd
import sqlalchemy
    
def getStaticInfo(dublin_stations_test, engine, conn):  
    df_query = pd.read_sql_query('SELECT * FROM static ORDER BY number desc', engine)
    query_json = df_query.to_json(orient='records')

    with open('templates/static_data.json', 'w') as f:
        f.write(query_json)

    print(query_json)

    
def main():
    from API_scraper import api_token, api_url_base, get_contracts_info

    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    conn = engine.connect()
    
    static_test = get_contracts_info()
    
    getStaticInfo(static_test, engine, conn)


if __name__ == "__main__":
    main()
