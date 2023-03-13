import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import Circuits, Constructors

# use this method to return to home page
@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# use this method to go to schedule pahe
@app.route('/schedule', methods=['POST'])
def schedule():
   print('Navigate to schedule.html')
   return render_template('schedule.html')

# use this method to return to standing page
@app.route('/standing', methods=['POST'])
def standing():
   print('Navigate to standing.html')
   return render_template('standing.html')

# use this method to return to simulate page
@app.route('/simulate', methods=['POST'])
def simulate():
   print('Navigate to simulate.html')
   return render_template('simulate.html')


if __name__ == '__main__':
   app.run()