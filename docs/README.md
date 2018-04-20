## Dublin Bikes Project

Our deliverable project is a web application that displays occupancy and weather information for Dublin Bikes.
This project collected data through the API, manages and stores data in an RDS DB on AWS, 
Displays Bike Stations on a map and shows occupancy and weather information.

## Getting Started

To run our project you will need to go to the following URL:

ec2-35-162-44-199.us-west-2.compute.amazonaws.com:5000

Note: Below is the link to our GitHub repository for this project
https://github.com/teamforsoft/SE_group_project
        

## Motivation

The motivation of our project is to display occupancy and weather information for Dublin Bikes, to predict the number of bikes available for a particular day and time (based on wind speed, temperature and on rain status) and to show pie charts and bar charts to this effect. This project also displays Bike Stations on a map which shows the occupancy and weather information. This information is then displayed in a clear, human readable, pleasing format 

## Installation

Firstly the project will need to be cloned from GitHub.   
Our project is organized in the following structure:
	SE_group_project
        /Docs
                /Static
                Sprint_backlogs
                TeamWriteUps
		/src
			/se_group_project
                __init__.py     
                config.py                    
                nohup.out               
                updateStaticData.py
                /__pycache__    
                connect_to_sqlite.py         
                run.py                  
                views.py
                /analytics      
                /DB_backup                  
                /static
                API_scraper.py  
                logger                       
                static_sqlite_table.py
                check_file      
                most_recent_station_data.db 
                /templates 
            /se_group_project.egg-info
        
        AUTHORS.rst  
        LICENSE.txt 
        MANIFEST.in  
        most_recent_station_data.db  
        README.rst  
        requirements.txt  
        setup.py  
        unit_tests.py


## Tests

Run the following command to perform the automated tests:

python -m unittest unit_tests.py

To run the tests in more detail run the following command:

python -m unittest -v unit_tests.py
 
        
## Contributors

Robert De Bhal 12751005
Orla Gartland  17204139 
Fatima Mohamed 17205708


