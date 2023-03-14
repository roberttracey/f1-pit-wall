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
   for con in constructors:
      constructor = Constructor()
      constructor.constructorId = con[0]
      constructor.constructorRef = con[1]
      constructor.name = con[2]
      constructor.nationality = con[3]
      constructor.url = con[4]
      db.session.add(constructor)
      constructorCount += 1   
   db.session.commit()
   print(constructorCount, 'constructors have been added!')  

   print('Importing constructor results ...')
   # set counter.
   constructorresultsCount = 0
   from data import constructorresults
   # sample: [1,18,1,14,None]
   for conres in constructorresults:
      constructorresult = ConstructorResult()
      constructorresult.constructorResultsId = conres[0]
      constructorresult.raceId = conres[1]
      constructorresult.constructorId = conres[2]
      constructorresult.points = conres[3]
      constructorresult.status = conres[4]
      db.session.add(constructorresult)
      constructorresultsCount += 1    
   db.session.commit() 
   print(constructorresultsCount, 'constructor results have been added!')
   
   # return to home page.
   return render_template('index.html')

# use this method to return to simulate page.
@app.route('/simulate', methods=['POST'])
def simulate(): 
   print('Navigate to simulate.html')
   return render_template('simulate.html')


if __name__ == '__main__':
   app.run()