# import the required modules.
import math
import os
from random import randrange
import numpy as np
from datetime import date
from datetime import datetime, timedelta
from markupsafe import Markup
import jinja2
from jinja2 import Environment
import fastf1
import pandas as pd
from datetime import datetime
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_wtf.csrf import CSRFProtect
from classes import RaceOrder, Simulation, LapGraph
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, text
from sqlalchemy import create_engine, Table, Column, Integer, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import requests


# create default race. 
simulation = Simulation(0, 0, 830)
lap_graph = LapGraph(0, '', [])

# check if ff1 cache folder exists.
ff1_cache = 'fastf1'
if os.path.exists(ff1_cache) == False:
   # if not, make it.
   os.mkdir(ff1_cache)
else:
   print('Cache folder found!')
# set ff1 cache location.
fastf1.Cache.enable_cache(ff1_cache) 

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

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

# use this custoim filter to display timedelta. 
def format_timedelta(value):  
    if value == 'NaT':
       return '00:00.000'
    # convert string value to timedelta. 
    td = pd.to_timedelta(value)
    # calculate huour, minute, seeond and milliseconds.
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return '{:02}:{:02}.{:03}'.format(int(minutes), int(seconds), milliseconds)

def timedelta_to_unix(laptime):
   td = pd.to_timedelta(laptime)   
   unix_time = (td - datetime.timedelta(0)).total_seconds()
   return unix_time

def timedelta_to_seconds(laptime):
   if laptime == 'NaT':
       return 0
   td = pd.to_timedelta(laptime)   
   return td.total_seconds()

def timedelta_to_milliseconds(laptime):
   if laptime == 'NaT':
       return 0
   td = pd.to_timedelta(laptime)   
   return td.total_seconds() * 1000
   

def ordinal(value):
    suffix = 'th' if 11 <= value % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
    return f'{value}{suffix}'

# add custom filters to app. 
app.jinja_env.filters['format_timedelta'] = format_timedelta
app.jinja_env.filters['ordinal'] = ordinal

# use this method to retrieve data using sql queries. 
def query_db(query):
   # create engine. 
   engine = create_engine(app.config.get('DATABASE_URI'))
   # define SQL query
   query = text(query)
   # execute query
   with engine.connect() as conn:
      result = conn.execute(query)
   # clean up database connection
   engine.dispose()
   return result

# use this method to return to home page.
@app.route('/')
@csrf.exempt
def index():
   # define sql query
   races_query = 'SELECT DISTINCT r.raceid, r.date, r.name FROM laps l, races r WHERE l.raceid = r.raceid ORDER BY r.raceid DESC LIMIT 8;'
   # get data.
   recent_races = query_db(races_query)
   # get race count.
   races_count = Lap.query.group_by(Lap.raceId).count()
   # get driver count.
   driver_count = Driver.query.group_by(Driver.driverId).count()
   # get teams count.
   team_count = Constructor.query.group_by(Constructor.constructorId).count()
   # print to console. 
   print('Request for index page received')
   # go to index page, and send race data. 
   return render_template('index.html', recent_races=recent_races, races_count=races_count, driver_count=driver_count, team_count=team_count)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# use this method to go to races page.
@app.route('/races', methods=['GET', 'POST'])
@csrf.exempt
def races():
   # get races from db
   # races = Race.query.where(Race.year == 2023).all()
   races = Race.query.where(Race.year >= 2019).all()
   print('Navigate to races.html')
   return render_template('races.html', races=races)

@app.route('/simulate/<int:race_id>', methods=['GET', 'POST'])
@csrf.exempt
def simulate(race_id):
   # set simulation values.
   global simulation
   simulation.lap = 1
   # reset graph
   lap_graph._laptimes = []
   simulation.raceId = race_id
   # get new simulation values. 
   lap = simulation.lap
   raceId = simulation.raceId
   driverId = simulation.driver
   # get race information. 
   race = Race.query.where(Race.raceId == race_id).first()
   # get circuit info. 
   circuit = Circuit.query.where(Circuit.circuitId == race.circuitId).first()
   # get default driver information. 
   driver = Driver.query.where(Driver.driverId == driverId).first()
   # get qualifying position. 
   qual_position = Qualifying.query.where(Qualifying.raceId == race_id, Qualifying.driverId == driverId).first()
   print('Starting simulation:', raceId)
   return render_template('simulate.html', race=race, circuit=circuit, driver=driver, qual_position=qual_position.position)


@app.route('/update_race_order', methods=['GET', 'POST'])
@csrf.exempt
def update_race_order():
   # get new simulation values. 
   global simulation
   lap = simulation.lap
   raceId = simulation.raceId
   # get lap data. 
   race_order = Lap.query.where(Lap.raceId == raceId, Lap.lapnumber == lap).order_by(Lap.time).all()    
   # calculate gaps between drivers. 
   data = calculate_interval(race_order.copy())
   # format data for json. 
   data = [row.as_dict() for row in data]
   # increment lap number. 
   simulation.incrementLap()
   print('Updating race order ...', lap) 
   return jsonify(data)

@app.route('/update_lap_graph', methods=['GET', 'POST'])
@csrf.exempt
def update_lap_graph():
   global simulation
   # get new simulation values. 
   lap = simulation.lap
   raceId = simulation.raceId
   driver = get_driver_code(simulation.driver)
   # get lap data. 
   result = Lap.query.where(Lap.raceId == raceId, Lap.lapnumber == lap, Lap.driver == driver).first()
   # add data to graph object.    
   lap_graph._lapnumber = result.lapnumber
   lap_graph._driver = result.driver
   lap_graph.add_time(timedelta_to_milliseconds(result.laptime))
   return jsonify(lap_graph.as_dict())

# use this method during a simulation to get the selected drivers position. 
def current_position(race_order):
   global simulation
   # get driverid, 
   driverId = simulation.driver
   # set default position to first. 
   pos = 1
   driver_pos = 1
   # loop current race order. 
   for order in race_order:
      if order.driverId == driverId:
         driver_pos = pos
         break
      else:
         pos = pos + 1

   return driver_pos

@app.route('/update_fastest_laps', methods=['GET', 'POST'])
@csrf.exempt
def update_fastest_laps():
   global simulation
   # get new simulation values. 
   lap = simulation.lap
   raceId = simulation.raceId
   # get fastest laps. 
   fastest_laps = Lap.query.filter(Lap.raceId == raceId, Lap.lapnumber <= lap, Lap.laptime != 'NaT').order_by(Lap.laptime).limit(5).all()    
   # format data for json. 
   fastest_laps = [row.as_dict() for row in fastest_laps]
   print('Updating fastest laps ...', lap) 
   return jsonify(fastest_laps)

def format_gap(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return '{:02}:{:02}.{:03}'.format(int(minutes), int(seconds), milliseconds)

def calculate_interval(data):
   # create array to store gaps. 
   time_diffs = []
   # set previous time to leaders time so gap is zero. 
   prev_time = pd.to_timedelta(data[0].time)
   leader = pd.to_timedelta(data[0].time)
   # loop data to calculate gaps. 
   for lap in data:
      # convert time to timedelta. 
      curr_time = pd.to_timedelta(lap.time)
      # calculate difference. 
      time_diff = curr_time - prev_time
      behind = curr_time - leader
      # create new race order object.       
      race_order = RaceOrder(lap.lapnumber, lap.driver, lap.team, lap.compound, lap.tyrelife, lap.time, format_gap(time_diff), format_gap(behind))
      # add race order to array. 
      time_diffs.append(race_order)
      # set previous value to current value for next calculation. 
      prev_time = curr_time

   return time_diffs

# use this method to go to drivers page.
@app.route('/drivers', methods=['GET', 'POST'])
@csrf.exempt
def drivers():
   # get drivers from db
   drivers = Driver.query.where().all()
   print('Navigate to drivers.html')
   return render_template('drivers.html', drivers=drivers)

# use this method to go to drivers page.
@app.route('/teams', methods=['GET', 'POST'])
@csrf.exempt
def teams():
   # get teams from db
   teams = Constructor.query.where().all()
   print('Navigate to teams.html')
   return render_template('teams.html', teams=teams)

@app.route('/races/<int:year>', methods=['GET', 'POST'])
@csrf.exempt
def get_races(year):
   # get races from db
   races = Race.query.where(Race.year == year).all()
   print('Update races for year', year)
   return render_template('races.html', races=races)


# use this method to return to standing page.
@app.route('/standing', methods=['GET', 'POST'])
@csrf.exempt
def standing():
   print('Navigate to standing.html')
   return render_template('standing.html')

# use this method to return to standing page.
@app.route('/settings', methods=['GET', 'POST'])
@csrf.exempt
def settings():
   print('Navigate to settings.html')
   return render_template('settings.html')

# use this method to return to standing page.
@app.route('/import_laps', methods=['POST'])
@csrf.exempt
def import_laps():
   # get last race in laps. 
   last_lap = Lap.query.order_by(Lap.lapId.desc()).limit(1).first()
   # if table is empty, start importing from 2019.
   if last_lap is None:
      start_date = '2019-03-01'
   else:
      # get details of last race. 
      last_race = Race.query.where(Race.raceId == last_lap.raceId).limit(1).first()    
      start_date = last_race.date
   # get races using year, round and date before today. 
   races = Race.query.where(Race.date > start_date, Race.date <= date.today()).all()
   print('races:', races)
   # loop races and import data. 
   for r in races:
      # get qualy results. 
      get_qualifying(r.year, r.round)
      # get new constructor standings
      get_constructor_standings(r.year, r.round)
      # get new driver standings
      get_driver_standings(r.year, r.round)
      # get pitstops
      get_pitstops(r.year, r.round)
      # get race results
      get_results(r.year, r.round)
      # get sprint results
      get_sprint_results(r.year, r.round)
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
   return redirect(url_for('index'))

# use this method to return to standing page.
@app.route('/import_data', methods=['POST'])
@csrf.exempt
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

   # print('Importing constructor results ...')
   # from data import constructorresults
   # # define table columns.
   # columns = ['constructorResultsId', 'raceId', 'constructorId', 'points', 'status']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(constructorresults, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='constructorresults', con=engine, if_exists='append', index=False)

   # print('Importing constructor standings  ...')
   # from data import constructorstandings
   # # define table columns.
   # columns = ['constructorStandingsId', 'raceId', 'constructorId', 'points', 'position', 'positionText', 'wins']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(constructorstandings, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='constructorstandings', con=engine, if_exists='append', index=False)

   # print('Importing driver standings ...')
   # from data import driverstandings
   # # define table columns.
   # columns = ['driverStandingsId', 'raceId', 'driverId', 'points', 'position', 'positionText', 'wins']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(driverstandings, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='driverstandings', con=engine, if_exists='append', index=False)

   # print('Importing pit stops ...')
   # from data import pitstops
   # # define table columns.
   # columns = ['raceId', 'driverId', 'stop', 'lap', 'time', 'duration', 'milliseconds']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(pitstops, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='pitstops', con=engine, if_exists='append', index=False)

   # print('Importing qualifying ...')
   # from data import qualifying
   # # define table columns.
   # columns = ['qualifyId', 'raceId', 'driverId', 'constructorId', 'number', 'position', 'q1', 'q2', 'q3']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(qualifying, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='qualifying', con=engine, if_exists='append', index=False)

   # print('Importing race results ...')
   # from data import results01, results02
   # # define table columns.
   # columns = ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed','statusId']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(results01, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='results', con=engine, if_exists='append', index=False)   

   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(results02, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='results', con=engine, if_exists='append', index=False)  

   # print('Importing sprint results ...')
   # from data import sprintresults
   # # define table columns.
   # columns = ['sprintResultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'fastestLapTime', 'statusId']
   # # create the pandas dataframe with column name is provided explicitly
   # df = pd.DataFrame(sprintresults, columns=columns)   
   # # insert dataframe into database.
   # df.to_sql(name='sprintresults', con=engine, if_exists='append', index=False)

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
   return redirect(url_for('index'))

def get_qualifying(year, round):
    # generate url. 
   url = f"http://ergast.com/api/f1/{year}/{round}/qualifying.json"
   payload={}
   headers = {}
   # send request.
   response = requests.request("GET", url, headers=headers, data=payload)
   # parse json.
   data = json.loads(response.text)
   # qualifying results as array. 
   results = data['MRData']['RaceTable']['Races'][0]['QualifyingResults']
   # get race id.
   race_id = get_raceid(year, round)
   # loop qualy results and get attributes. 
   for result in results:
      # create qualifying object. 
      qualy = Qualifying()
      # set values.          
      qualy.raceId = race_id
      qualy.driverId = get_driverid(result['Driver']['driverId'])
      qualy.constructorId = get_constructorid(result['Constructor']['constructorId'])
      qualy.number = result['number']
      qualy.position = result['position']
      if 'Q1' in result:
         qualy.q1 = result['Q1']
      else:
         qualy.q1 = ''
      if 'Q2' in result:
         qualy.q2 = result['Q2']
      else:
         qualy. q2 = ''
      if 'Q3' in result:
         qualy.q3 = result['Q3']
      else:
         qualy.q3 = ''    
      # add to db.
      db.session.add(qualy) 
   # commit chnages to db. 
   db.session.commit()

def get_constructor_standings(year, round):
   # generate url. 
   url = f"http://ergast.com/api/f1/{year}/{round}/constructorStandings.json"
   payload={}
   headers = {}
   # send request.
   response = requests.request("GET", url, headers=headers, data=payload)
   # parse json.
   data = json.loads(response.text)
   # qualifying results as array. 
   results = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
   # get race id.
   race_id = get_raceid(year, round)
   for result in results:
      # create standing object. 
      standing = ConstructorStanding()
      # set values.          
      standing.raceId = race_id
      standing.constructorId = get_constructorid(result['Constructor']['constructorId'])
      standing.points = result['points']
      standing.position = result['position']
      standing.positionText = result['positionText']
      standing.wins = wins = result['wins']
      # add to db.
      db.session.add(standing) 
   # commit chnages to db. 
   db.session.commit()

def get_driver_standings(year, round):
   # generate url. 
   url = f"http://ergast.com/api/f1/{year}/{round}/driverStandings.json"
   payload={}
   headers = {}
   # send request.
   response = requests.request("GET", url, headers=headers, data=payload)
   # parse json.
   data = json.loads(response.text)
   # qualifying results as array. 
   results = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
   # get race id.
   race_id = get_raceid(year, round)
   for result in results:
      # create standing object. 
      standing = DriverStanding()
      # set values.          
      standing.raceId = race_id
      standing.driverId = get_driverid(result['Driver']['driverId'])
      standing.points = result['points']
      standing.position = result['position']
      standing.positionText = result['positionText']
      standing.wins = wins = result['wins']
      # add to db.
      db.session.add(standing) 
   # commit chnages to db. 
   db.session.commit()

def get_results(year, round):
   # generate url. 
   url = f"http://ergast.com/api/f1/{year}/{round}/results.json"
   payload={}
   headers = {}
   # send request.
   response = requests.request("GET", url, headers=headers, data=payload)
   # parse json.
   data = json.loads(response.text)
   # get race id.
   race_id = get_raceid(year, round)
   # get race results as array. 
   results = data['MRData']['RaceTable']['Races'][0]['Results']
   for result in results:
      race_result = Result()
      constructor_result = ConstructorResult()      
      race_result.raceId = race_id
      constructor_result.raceId = race_id      
      race_result.driverId = get_driverid(result['Driver']['driverId'])
      race_result.constructorId = get_constructorid(result['Constructor']['constructorId'])
      constructor_result.constructorId = get_constructorid(result['Constructor']['constructorId'])
      race_result.number = result['number']
      race_result.grid = result['grid']
      race_result.position = result['position']
      race_result.positionText = result['positionText']
      race_result.positionOrder = result['position']
      race_result.points = result['points']
      constructor_result.points = result['points']
      race_result.laps = result['laps']
      if 'Time' in result:
         race_result.time = result['Time']['time']
         race_result.milliseconds = result['Time']['millis']
      else:
         race_result.time = ''
         race_result.milliseconds = ''        
      if 'FastestLap' in result:
         race_result.fastestLap = result['FastestLap']['lap']
         race_result.rank = result['FastestLap']['rank']
         race_result.fastestLapTime = result['FastestLap']['Time']['time']
         race_result.fastestLapSpeed = result['FastestLap']['AverageSpeed']['speed']
      else:
         race_result.fastestLap = ''
         race_result.rank = ''
         race_result.fastestLapTime = ''
         race_result.fastestLapSpeed = ''        
      race_result.statusId = get_statusid(result['status'])
      constructor_result.statusId = get_statusid(result['status'])
      # add to db.
      db.session.add(race_result)
      db.session.add(constructor_result)  
   # commit chnages to db. 
   db.session.commit()

def get_sprint_results(year, round):
   # generate url. 
   url = f"http://ergast.com/api/f1/{year}/{round}/sprint.json"
   payload={}
   headers = {}
   # send request.
   response = requests.request("GET", url, headers=headers, data=payload)
   # parse json.
   data = json.loads(response.text)
   # get race id.
   race_id = get_raceid(year, round)
   # get race results as array. 
   if 'SprintResults' in data:
      results = data['MRData']['RaceTable']['Races'][0]['SprintResults']
      for result in results:
         sprint_result = SprintResult()
         constructor_result = ConstructorResult()      
         sprint_result.raceId = race_id
         constructor_result.raceId = race_id      
         sprint_result.driverId = get_driverid(result['Driver']['driverId'])
         sprint_result.constructorId = get_constructorid(result['Constructor']['constructorId'])
         constructor_result.constructorId = get_constructorid(result['Constructor']['constructorId'])
         sprint_result.number = result['number']
         sprint_result.grid = result['grid']
         sprint_result.position = result['position']
         sprint_result.positionText = result['positionText']
         sprint_result.positionOrder = result['position']
         sprint_result.points = result['points']
         constructor_result.points = result['points']
         sprint_result.laps = result['laps']
         if 'Time' in result:
            sprint_result.time = result['Time']['time']
            sprint_result.milliseconds = result['Time']['millis']
         else:
            sprint_result.time = ''
            sprint_result.milliseconds = ''        
         if 'FastestLap' in result:
            sprint_result.fastestLap = result['FastestLap']['lap']
            sprint_result.fastestLapTime = result['FastestLap']['Time']['time']
         else:
            sprint_result.fastestLap = ''
            sprint_result.fastestLapTime = ''       
         sprint_result.statusId = get_statusid(result['status'])
         constructor_result.statusId = get_statusid(result['status'])
         # add to db.
         db.session.add(sprint_result)
         db.session.add(constructor_result)  
      # commit changes to db. 
      db.session.commit()

def get_pitstops(year, round):
    length = 30
    offset = 0
    while length == 30:
      # generate url. 
      url = f"http://ergast.com/api/f1/{year}/{round}/pitstops.json?limit=30&offset={offset}"
      payload={}
      headers = {}
      # send request.
      response = requests.request("GET", url, headers=headers, data=payload)
      # parse json.
      data = json.loads(response.text)
      # get race results as array. 
      if 'PitStops' in data:
         pitstops = data['MRData']['RaceTable']['Races'][0]['PitStops']
         # get length of the latest response. 
         length = len(pitstops)    
         for pit in pitstops:
            pitstop = PitStop()
            pitstop.raceId = get_raceid(year, round)
            pitstop.driverId = get_driverid(pit['driverId'])
            pitstop.stop = pit['stop']
            pitstop.lap = pit['lap']
            pitstop.time = pit['time'] 
            pitstop.duration = pit['duration']
            pitstop.milliseconds = remove_colon_and_dot(pit['duration'])
            # add to db.
            db.session.add(pitstop)      
         # increase offset
         offset += 30
         # commit changes to db. 
         db.session.commit()
      else:
         length = 0

# api prodives inconsistent format for duration, so use this to convert to milliseconds. 
def remove_colon_and_dot(input_string):    
    # replace ':' with an empty string
    result_string = input_string.replace(':', '')    
    # replace '.' with an empty string
    result_string = result_string.replace('.', '')    
    # return the resulting string
    return result_string 

# use this method to get race id by year and round. 
def get_raceid(year, round):
   race = Race.query.where(Race.year == year, Race.round == round).first()
   return race.raceId

# use this method to get driver id by driver ref.
def get_driverid(driver_ref):
   driver = Driver.query.where(Driver.driverRef == driver_ref).first()
   return driver.driverId

# use this method to get driver id by driver ref.
def get_driver_code(driverid):
   driver = Driver.query.where(Driver.driverId == driverid).first()
   return driver.code

# use this method to get constructor id by constructor ref.
def get_constructorid(constructor_ref):
   constructor = Constructor.query.where(Constructor.constructorRef == constructor_ref).first()
   return constructor.constructorId

# use this method to get status id from status.
def get_statusid(status_ref):
   status = Status.query.where(Status.status == status_ref).first()
   return status.statusId

if __name__ == '__main__':
   app.run()