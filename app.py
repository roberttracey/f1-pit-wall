# import the required modules.
import math
import os
from datetime import date
import fastf1
import pandas as pd
from datetime import datetime
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# check if ff1 cache folder exists.
ff1_cache = 'fastf1'
if os.path.exists(ff1_cache) == False:
   # if not, make it.
   os.mkdir(ff1_cache)
else:
   print('Cache folder found!')

# set ff1 cache location.
fastf1.Cache.enable_cache('fastf1') 

app = Flask(__name__, static_folder='static')

# use this code to determine of we are working locally or in azure.
if 'WEBSITE_HOSTNAME' not in os.environ: # website_hostname exists only in production environment.
    # local development, where we'll use environment variables.
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # load database string from production file.
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

# enable flask-migrate commands "flask db init/migrate/upgrade" to work.
migrate = Migrate(app, db)

# import must be done after db initialization due to circular import issue.
from models import Circuit, ConstructorResult, ConstructorStanding, Race, Season, Constructor, DriverStanding, Driver, PitStop, Qualifying, Result, SprintResult, Status, Lap, TrackStatus

# use this method to return to home page.
@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# use this method to go to schedule page.
@app.route('/schedule', methods=['POST'])
def schedule():
   print('Navigate to schedule.html')
   return render_template('schedule.html')


# use this method to return to standing page.
@app.route('/standing', methods=['POST'])
def standing():
   print('Navigate to standing.html')
   return render_template('standing.html')

# use this method to return to standing page.
@app.route('/settings', methods=['POST'])
def settings():
   print('Navigate to settings.html')
   return render_template('settings.html')

# use this method to return to standing page.
@app.route('/import_laps', methods=['POST'])
def import_laps():
   races = Race.query.where(Race.year >= 2019, Race.date <= date.today()).all()
   # get_session(2022, 'Bahrain', 'Race')
   # print('Importing laps ...')
   for r in races:
      # print(r.year, r.round, r.date)
      session = fastf1.get_session(r.year, r.round, 'Race')
      print('Importing:', r.year, r.name)
      # load the session
      session.load()
      # get laps for given session
      laps = session.laps
      # store session data in dataframe
      df = pd.DataFrame(laps)
      # df = df.reset_index()  # make sure indexes pair with number of rows
      for i in df.index:
         lap = Lap()
         lap.raceId = r.raceId
         lap.time = df['Time'][i]
         lap.driver = df['Driver'][i]
         lap.drivernumber = df['DriverNumber'][i]
         lap.laptime = df['LapTime'][i]
         lap.lapnumber = df['LapNumber'][i]
         lap.stint = df['Stint'][i]
         lap.pitouttime = df['PitOutTime'][i]
         lap.pitintime = df['PitInTime'][i]
         lap.sector1time = df['Sector1Time'][i]
         lap.sector2time = df['Sector2Time'][i]
         lap.sector3time = df['Sector3Time'][i]
         lap.sector1sessiontime = df['Sector1SessionTime'][i]
         lap.sector2sessiontime = df['Sector2SessionTime'][i]
         lap.sector3sessiontime = df['Sector3SessionTime'][i]
         # avoid 'nan' value as they are no allow in MySQL.
         if math.isnan (df['SpeedI1'][i]):
            lap.speedi1 = 0
         else:
            lap.speedi1 = df['SpeedI1'][i]
         # lap.speedi2 = df['SpeedI2'][i]
         if math.isnan (df['SpeedI2'][i]):
            lap.speedi2 = 0
         else:
            lap.speedi2 = df['SpeedI2'][i]
         # lap.speedfl = df['SpeedFL'][i]
         if math.isnan (df['SpeedFL'][i]):
            lap.speedfl = 0
         else:
            lap.speedfl = df['SpeedFL'][i]
         # lap.speedst = df['SpeedST'][i]
         if math.isnan (df['SpeedST'][i]):
            lap.speedst = 0
         else:
            lap.speedst = df['SpeedST'][i]         
         # lap.ispersonalbest = df['IsPersonalBest'][i]
         if math.isnan (df['IsPersonalBest'][i]):
            lap.ispersonalbest = 0
         else:
            lap.ispersonalbest = df['IsPersonalBest'][i]            
         lap.compound = df['Compound'][i]
         # lap.tyrelife = df['TyreLife'][i]
         if math.isnan (df['TyreLife'][i]):
            lap.tyrelife = 0
         else:
            lap.tyrelife = df['TyreLife'][i] 
         # lap.freshtyre = df['FreshTyre'][i]
         if math.isnan (df['FreshTyre'][i]):
            lap.freshtyre = 0
         else:
            lap.freshtyre = df['FreshTyre'][i]  
         lap.team = df['Team'][i]
         lap.lapstarttime = df['LapStartTime'][i]
         lap.lapstartdate = df['LapStartDate'][i]
         lap.trackstatus = df['TrackStatus'][i]
         # lap.isaccurate = df['IsAccurate'][i]
         if math.isnan (df['IsAccurate'][i]):
            lap.isaccurate = 0
         else:
            lap.isaccurate = df['IsAccurate'][i]
         db.session.add(lap) 
      db.session.commit()
      
   # return to home page.
   return render_template('settings.html')

# use this method to return to standing page.
@app.route('/import_data', methods=['POST'])
def import_data():
   # create engine.
   engine = create_engine(app.config.get('DATABASE_URI'))
   print('Data import requested.')    

   print('Importing seasons ...')  
   from data import seasons
   # define table columns.
   columns = ['year', 'url']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(seasons, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='seasons', con=engine, if_exists='append', index=False)

   print('Importing circuits ...')
   from data import circuits
   # define table columns.
   columns = ['circuitId', 'circuitRef', 'name', 'location', 'country', 'lat', 'lng', 'alt', 'url']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(circuits, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='circuits', con=engine, if_exists='append', index=False)  

   print('Importing races ...')
   from data import races
   # define table columns.
   columns = ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'sprint_time']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(races, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='races', con=engine, if_exists='append', index=False) 

   print('Importing constructors ...')
   from data import constructors
   # define table columns.
   columns = ['constructorId', 'constructorRef', 'name', 'nationality', 'url']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(constructors, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='constructors', con=engine, if_exists='append', index=False)  

   print('Importing drivers ...')
   from data import drivers
   # define table columns.
   columns = ['driverId', 'driverRef', 'number', 'code', 'forename', 'surname', 'dob', 'nationality', 'url']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(drivers, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='drivers', con=engine, if_exists='append', index=False) 

   print('Importing status ...')
   from data import status
   # define table columns.
   columns = ['statusId', 'status']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(status, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='status', con=engine, if_exists='append', index=False)  

   print('Importing constructor results ...')
   from data import constructorresults
   # define table columns.
   columns = ['constructorResultsId', 'raceId', 'constructorId', 'points', 'status']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(constructorresults, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='constructorresults', con=engine, if_exists='append', index=False)

   print('Importing constructor standings  ...')
   from data import constructorstandings
   # define table columns.
   columns = ['constructorStandingsId', 'raceId', 'constructorId', 'points', 'position', 'positionText', 'wins']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(constructorstandings, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='constructorstandings', con=engine, if_exists='append', index=False)

   print('Importing driver standings ...')
   from data import driverstandings
   # define table columns.
   columns = ['driverStandingsId', 'raceId', 'driverId', 'points', 'position', 'positionText', 'wins']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(driverstandings, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='driverstandings', con=engine, if_exists='append', index=False)

   print('Importing pit stops ...')
   from data import pitstops
   # define table columns.
   columns = ['raceId', 'driverId', 'stop', 'lap', 'time', 'duration', 'milliseconds']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(pitstops, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='pitstops', con=engine, if_exists='append', index=False)

   print('Importing qualifying ...')
   from data import qualifying
   # define table columns.
   columns = ['qualifyId', 'raceId', 'driverId', 'constructorId', 'number', 'position', 'q1', 'q2', 'q3']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(qualifying, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='qualifying', con=engine, if_exists='append', index=False)

   print('Importing race results ...')
   from data import results01, results02
   # define table columns.
   columns = ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed','statusId']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(results01, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='results', con=engine, if_exists='append', index=False)   

   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(results02, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='results', con=engine, if_exists='append', index=False)  

   print('Importing sprint results ...')
   from data import sprintresults
   # define table columns.
   columns = ['sprintResultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'fastestLapTime', 'statusId']
   # create the pandas dataframe with column name is provided explicitly
   df = pd.DataFrame(sprintresults, columns=columns)   
   # insert dataframe into database.
   df.to_sql(name='sprintresults', con=engine, if_exists='append', index=False)

   # initialize data of lists.
   trackstatus = {'statusId': [1, 2, 3, 4, 5, 6, 7],
        'status': ['Track Clear', 'Yellow Flag', 'Unused', 'Safety Car', 'Red Flag', 'VSC', 'VSC Ending']}   
   # create dataframe
   df = pd.DataFrame(trackstatus)
   # insert dataframe into database.
   df.to_sql(name='trackstatus', con=engine, if_exists='append', index=False)

   # close the database connection
   engine.dispose()
   # return to home page.
   return render_template('settings.html')

# use this method to return to simulate page.
@app.route('/simulate', methods=['POST'])
def simulate(): 
   print('Navigate to simulate.html')
   return render_template('simulate.html')


if __name__ == '__main__':
   app.run()