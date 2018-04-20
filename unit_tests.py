import sys
sys.path.insert(0, "./src/se_group_project/")
#print(sys.path)
from se_group_project import API_scraper
import unittest
from unittest.mock import patch 
import requests
import sqlalchemy
import sqlite3
import pandas as pd
from unittest.mock import patch, MagicMock
api_token = '7e813fe2e25367cd1aa3c4403c764332448fce48' 
api_url_base = 'https://api.jcdecaux.com/vls/v1/'
from se_group_project import views


class TestMainFunctionality(unittest.TestCase):
    def test_MySQL_db_file(self):
        """test if occupancy table exists in local db file""" # connect to database
        engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
        conn = engine.connect() # these 2 lines are in API_scraper 
        df_query = pd.read_sql_query('SELECT * FROM static ORDER BY number desc limit 1', engine)
        if (df_query.shape[0]>0):
            gotData = True
        else:
            gotData  = False
        conn.close()
        self.assertEqual(gotData,  True,'connection to local db failed') 
	
    def test_local_db_file(self):
        """test if occupancy table exists in local db file"""# connect to database
        #https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
        #https://stackoverflow.com/questions/19622341/how-to-test-if-a-table-already-exists?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        enginesqlite = sqlite3.connect('most_recent_station_data.db')
        cur = enginesqlite.cursor()    # this is in views 
        table_name = "SELECT available_bikes FROM occupancy;"
        if (cur.execute(table_name ).fetchone()):
            gotData = True
        else:
            gotData  = False
        cur.close()
        self.assertEqual(gotData,  True,'connection to local db failed') 

    def test_JCDecaux_connection(self):
        """Test connection to JCDecaux API"""
        status_bikes= requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}'.format(api_token)).status_code
        self.assertEqual(status_bikes, 200,'connection to JCDecaux failed')
	
    def test_weather_connection(self):
        """Test connection to Open Weather Maps"""
        status_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&APPID=70ef396e3ce3949e0934b4428e41f453').status_code
        self.assertEqual(status_weather, 200,'connection to Open Weather Maps failed') 

		
"""
	@patch('mypackage.mymodule.pymysql')
	def test(self, mock_sql):
	#	self.assertIs(mypackage.mymodule.pymysql, mock_sql)
        self.assertIs(se_group_projeect.API_scraper.main.engine.pymysql, mock_sql)
		conn = Mock()
		mock_sql.connect.return_value = conn

		cursor      = MagicMock()
		mock_result = MagicMock()

		cursor.__enter__.return_value = mock_result
		cursor.__exit___              = MagicMock()

		conn.cursor.return_value = cursor

		connectDB()

		mock_sql.connect.assert_called_with('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')

		mock_result.execute.assert_called_with("sql request", ("user", "pass"))
"""
	


	

	
	
if __name__== '__main__':
    unittest.main()
	
	

	
	


			