from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
app = Flask(__name__)

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