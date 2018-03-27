from setuptools import setup

setup(name= "se_group_project",
      version="0.1",
      description= "Scraper for Dublin bikes", 
      url="https://github.com/orla-gartland/switch_lights",
      author="Orla Gartland", 
      author_email="orla.gartland@ucdconnect.ie",
      licence="GPL3", 
      packages= ['se_group_project'],
      entry_points ={
<<<<<<< HEAD
          'console_scripts':['scraper=se_group_project.API_scraper:main','host=se_group_project.run:run']
=======
          'console_scripts':['scraper=se_group_project.API_scraper:main,host=se_group_project.run:run']
>>>>>>> b50e1ba54aac1462543e93c0116a6fef0a479877
          }
      ##
    )
