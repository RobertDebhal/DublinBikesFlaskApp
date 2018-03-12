'''
Created on 12 Mar 2018

@author: robbie
'''
# source https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
import json
import requests
import datetime

api_token = '7e813fe2e25367cd1aa3c4403c764332448fce48' 
api_url_base = 'https://api.jcdecaux.com/vls/v1/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'apiKey {0}'.format(api_token)}

def get_contracts_info():

    api_url = '{0}contracts'.format(api_url_base)

    #response = requests.get(api_url, headers=headers)
    response = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={0}'.format(api_token))

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
dublin_stations_test = get_contracts_info()

if dublin_stations_test is not None:
    print("Here are the stations: ")
    for i in dublin_stations_test:
        #https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        print(i['name']+":",datetime.datetime.fromtimestamp(int(i['last_update'])/1000).strftime('%Y-%m-%d %H:%M:%S'),'available bikes:',i['available_bike_stands'])
else:
    print('[!] Request Failed')