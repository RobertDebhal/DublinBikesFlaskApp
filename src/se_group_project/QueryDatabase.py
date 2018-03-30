import json
import requests
import pandas as pd
import sqlalchemy
from flask import jsonify
    
def getStaticInfo(engine, conn):  
    df_query = pd.read_sql_query('SELECT * FROM static ORDER BY number desc', engine)
    df_dict = df_query.to_dict(orient='records')
#     print(df_dict)
    print((df_dict))
#     print(df_dict)
#     with open('newinfo.text', 'w') as outfile:
#         outfile.write(df_dict)
#     query_json = df_query.to_json(orient='records')
#     print(query_json)
#     df_querydf_query
    

#     print(query_json)

    
def main():
    from API_scraper import api_token, api_url_base

    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    conn = engine.connect()
    
#     static_test = get_contracts_info()
    
    getStaticInfo( engine, conn)


if __name__ == "__main__":
    main()
