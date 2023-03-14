# import the required modules.
import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')


# use this code to determine of we are working locally or in azure.
# website_hostname exists only in production environment.
if 'WEBSITE_HOSTNAME' not in os.environ:
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
from models import Circuit, ConstructorResult, ConstructorStanding, Race, Season, Constructor, DriverStanding, Driver, LapTime, PitStop, Qualifying, Result, SprintResult, Status

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
@app.route('/import_data', methods=['POST'])
def import_data():
   print('Data import requested.')  
   print('Importing seasons ...')
   # set counter.
   seasonCount = 0
   from data import seasons
   # sample: [2009,'http://en.wikipedia.org/wiki/2009_Formula_One_season']
   for sn in seasons:
      season = Season()
      season.year = sn[0]
      season.url = sn[1]
      db.session.add(season)
      seasonCount += 1   
   db.session.commit()
   print(seasonCount, 'seasons have been added!')

   print('Importing circuits ...')
   # set counter.
   circuitCount = 0
   from data import circuits
   # sample: [1,'albert_park','Albert Park Grand Prix Circuit','Melbourne','Australia',-37.8497,144.968,10,'http://en.wikipedia.org/wiki/Melbourne_Grand_Prix_Circuit']
   for cir in circuits:
      circuit = Circuit()
      circuit.circuitId = cir[0]
      circuit.circuitRef = cir[1]
      circuit.name = cir[2]
      circuit.location = cir[3]
      circuit.country = cir[4]
      circuit.lat = cir[5]
      circuit.lng = cir[6]
      circuit.alt = cir[7]
      circuit.url = cir[8]
      db.session.add(circuit)
      circuitCount += 1   
   db.session.commit()
   print(circuitCount, 'circuits have been added!')
   

   print('Importing races ...')
   # set counter.
   raceCount = 0
   from data import races
   # sample: [1,2009,1,1,'Australian Grand Prix','2009-03-29','06:00:00','http://en.wikipedia.org/wiki/2009_Australian_Grand_Prix',None,None,None,None,None,None,None,None,None,None]
   for rs in races:
      race = Race()
      race.raceId = rs[0]
      race.year = rs[1]
      race.round = rs[2]
      race.circuitId = rs[3]
      race.name = rs[4]
      race.date = rs[5]
      race.time = rs[6]
      race.url = rs[7]
      race.fp1_date = rs[8]
      race.fp1_time = rs[9]
      race.fp2_date = rs[10]
      race.fp2_time = rs[11]
      race.fp3_date = rs[12]
      race.fp3_time = rs[13]
      race.quali_date = rs[14]
      race.quali_time = rs[15]
      race.sprint_date = rs[16]
      race.sprint_time = rs[17]
      db.session.add(race)
      raceCount += 1  
   db.session.commit() 
   print(raceCount, 'races have been added!')

   print('Importing constructors ...')
   # set counter.
   constructorCount = 0
   from data import constructors
   # sample: [1,'mclaren','McLaren','British','http://en.wikipedia.org/wiki/McLaren']
   for c in constructors:
      constructor = Constructor()
      constructor.constructorId = c[0]
      constructor.constructorRef = c[1]
      constructor.name = c[2]
      constructor.nationality = c[3]
      constructor.url = c[4]
      db.session.add(constructor)
      constructorCount += 1   
   db.session.commit()
   print(constructorCount, 'constructors have been added!')  

   print('Importing drivers ...')
   # set counter.
   driversCount = 0
   from data import drivers
   # sample: [855,'zhou',24,'ZHO','Guanyu','Zhou','1999-05-30','Chinese','http://en.wikipedia.org/wiki/Guanyu_Zhou']
   for d in drivers:
      driver = Driver()
      driver.driverId = d[0]
      driver.driverRef = d[1]
      driver.number = d[2]
      driver.code = d[3]
      driver.forename = d[4]
      driver.surname = d[5]
      driver.dob = d[6]
      driver.nationality = d[7]
      driver.url = d[8]
      db.session.add(driver)
      driversCount += 1    
   db.session.commit() 
   print(driversCount, 'drivers have been added!')

   print('Importing status ...')
   # set counter.
   statusCount = 0
   from data import status
   # sample: [1,'Finished']
   for s in status:
      stat = Status()
      stat.statusId = s[0]
      stat.status = s[1]
      db.session.add(stat)
      statusCount += 1    
   db.session.commit() 
   print(statusCount, 'statuses have been added!')

   print('Importing constructor results ...')
   # set counter.
   constructorresultsCount = 0
   from data import constructorresults
   # sample: [1,18,1,14,None]
   for c in constructorresults:
      constructorresult = ConstructorResult()
      constructorresult.constructorResultsId = c[0]
      constructorresult.raceId = c[1]
      constructorresult.constructorId = c[2]
      constructorresult.points = c[3]
      constructorresult.status = c[4]
      db.session.add(constructorresult)
      constructorresultsCount += 1    
   db.session.commit() 
   print(constructorresultsCount, 'constructor results have been added!')

   print('Importing constructor standings  ...')
   # set counter.
   constructorstandingsCount = 0
   from data import constructorstandings
   # sample: [1,18,1,14,1,'1',1]
   for c in constructorstandings:
      constructorstanding = ConstructorStanding()
      constructorstanding.constructorStandingsId = c[0]
      constructorstanding.raceId = c[1]
      constructorstanding.constructorId = c[2]
      constructorstanding.points = c[3]
      constructorstanding.position = c[4]
      constructorstanding.positionText = c[5]
      constructorstanding.wins = c[6]
      db.session.add(constructorstanding)
      constructorstandingsCount += 1    
   db.session.commit() 
   print(constructorstandingsCount, 'constructor standings have been added!')

   print('Importing driver standings ...')
   # set counter.
   driverstandingsCount = 0
   from data import driverstandings
   # sample: [1,18,1,10,1,'1',1]
   for d in driverstandings:
      driverstanding = DriverStanding()
      driverstanding.driverStandingsId = d[0]
      driverstanding.raceId = d[1]
      driverstanding.driverId = d[2]
      driverstanding.points = d[3]
      driverstanding.position = d[4]
      driverstanding.positionText = d[5]
      driverstanding.wins = d[6]
      db.session.add(driverstanding)
      driverstandingsCount += 1    
   db.session.commit() 
   print(driverstandingsCount, 'driver standings have been added!')

   print('Importing pit stops ...')
   # set counter.
   pitstopsCount = 0
   from data import pitstops
   # sample: [841,153,1,1,'17:05:23','26.898',26898]
   for ps in pitstops:
      pitstop = PitStop()
      pitstop.raceId = ps[0]
      pitstop.driverId = ps[1]
      pitstop.stop = ps[2]
      pitstop.lap = ps[3]
      pitstop.time = ps[4]
      pitstop.duration = ps[5]
      pitstop.milliseconds = ps[6]
      db.session.add(pitstop)
      pitstopsCount += 1    
   db.session.commit() 
   print(pitstopsCount, 'pit stops have been added!')

   print('Importing qualifying ...')
   # set counter.
   qualifyingCount = 0
   from data import qualifying
   # sample: [1,18,1,1,22,1,'1:26.572','1:25.187','1:26.714']
   for q in qualifying:
      quali = Qualifying()
      quali.qualifyId = q[0]
      quali.raceId = q[1]
      quali.driverId = q[2]
      quali.constructorId = q[3]
      quali.number = q[4]
      quali.position = q[5]
      quali.q1 = q[6]
      quali.q2 = q[7]
      quali.q3 = q[8]
      db.session.add(quali)
      qualifyingCount += 1    
   db.session.commit() 
   print(qualifyingCount, 'qualifying sessions have been added!')

   print('Importing results 01 ...')
   # set counter.
   results01Count = 0
   from data import results01
   # sample: [1,18,1,1,22,1,1,'1',1,10,58,'1:34:50.616',5690616,39,2,'1:27.452','218.300',1]
   for r in results01:
      result = Result()
      result.resultId = r[0]
      result.raceId = r[1]
      result.driverId = r[2]
      result.constructorId = r[3]
      result.number = r[4]
      result.grid = r[5]
      result.position = r[6]
      result.positionText = r[7]
      result.positionOrder = r[8]
      result.points = r[9]
      result.laps = r[10]
      result.time = r[11]
      result.milliseconds = r[12]
      result.fastestLap = r[13]
      result.rank = r[14]
      result.fastestLapTime = r[15]
      result.fastestLapSpeed = r[16]
      result.statusId = r[17]
      db.session.add(result)
      results01Count += 1    
   db.session.commit() 
   print(results01Count, 'results 01 have been added!')

   print('Importing results 02 ...')
   # set counter.
   results02Count = 0
   from data import results02
   # sample: [1,18,1,1,22,1,1,'1',1,10,58,'1:34:50.616',5690616,39,2,'1:27.452','218.300',1]
   for r in results02:
      result = Result()
      result.resultId = r[0]
      result.raceId = r[1]
      result.driverId = r[2]
      result.constructorId = r[3]
      result.number = r[4]
      result.grid = r[5]
      result.position = r[6]
      result.positionText = r[7]
      result.positionOrder = r[8]
      result.points = r[9]
      result.laps = r[10]
      result.time = r[11]
      result.milliseconds = r[12]
      result.fastestLap = r[13]
      result.rank = r[14]
      result.fastestLapTime = r[15]
      result.fastestLapSpeed = r[16]
      result.statusId = r[17]
      db.session.add(result)
      results02Count += 1    
   db.session.commit() 
   print(results02Count, 'results 02 have been added!')

   print('Importing sprint results ...')
   # set counter.
   sprintresultsCount = 0
   from data import sprintresults
   # sample: [1,1061,830,9,33,2,1,'1',1,3,17,'25:38.426',1538426,14,'1:30.013',1]
   for sr in sprintresults:
      sprintresult = SprintResult()
      sprintresult.sprintResultId = sr[0]
      sprintresult.raceId = sr[1]
      sprintresult.driverId = sr[2]
      sprintresult.constructorId = sr[3]
      sprintresult.number = sr[4]
      sprintresult.grid = sr[5]
      sprintresult.position = sr[6]
      sprintresult.positionText = sr[7]
      sprintresult.positionOrder = sr[8]
      sprintresult.points = sr[9]
      sprintresult.laps = sr[10]
      sprintresult.time = sr[11]
      sprintresult.milliseconds = sr[12]
      sprintresult.fastestLap = sr[13]
      sprintresult.fastestLapTime = sr[14]
      sprintresult.statusId = sr[15]
      db.session.add(sprintresult)
      sprintresultsCount += 1    
   db.session.commit() 
   print(sprintresultsCount, 'sprint results have been added!')

   # return to home page.
   return render_template('index.html')

# use this method to return to simulate page.
@app.route('/simulate', methods=['POST'])
def simulate(): 
   print('Navigate to simulate.html')
   return render_template('simulate.html')


if __name__ == '__main__':
   app.run()