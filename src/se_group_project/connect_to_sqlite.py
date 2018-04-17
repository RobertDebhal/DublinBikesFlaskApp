from API_scraper import make_rain_table
import sqlalchemy
import sqlite3


engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()#creating local sqlite connection/database for quicker response to marker click queries
enginesqlite = sqlite3.connect('most_recent_station_data.db')

make_rain_table(enginesqlite,conn)
