import pandas as pd
import sqlite3
import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()#creating local sqlite connection/database for quicker response to marker click queries
enginesqlite = sqlite3.connect('most_recent_station_data.db')

static_df = pd.read_sql_query('SELECT s.number,s.lat,s.lng FROM static s;',con=conn)
static_df.to_sql(name = 'static', con = enginesqlite, if_exists='replace',index=False, flavor='sqlite')