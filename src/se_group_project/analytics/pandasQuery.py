import pandas as pd
import sqlalchemy


engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()#creating local sqlite connection/database for quicker response to marker click queries

analytics_df = pd.read_sql_query('SELECT * FROM dynamic d, weather w WHERE d.latest_weather = w.date;',con=conn)

analytics_df.to_csv('analytics.csv')
