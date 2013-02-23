import os
from flask import Flask, request, session, url_for, render_template, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient

# quickstart database
from flask.ext.sqlalchemy import SQLAlchemy

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

app = Flask(__name__)

# determine database location based on environment
if 'YOUR_ENV_VAR' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.config['SECRET_KEY'] = 'something secret'
app.config.update( DEBUG = True )

# contains functions/helpers form sqlalchemy and sqlalchemy.orm
db = SQLAlchemy(app)

# migrate database -- doesn't overwrite tables
db.create_all()

#-------------------------------------------------------------------------------
# Models
#-------------------------------------------------------------------------------

# declarative modelling
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(25), unique=True)
    phone_number = db.Column(db.String(20), unique=True)

    def __init__(self, username, email, password, phone_number):

        # TODO: figure out how to validate input

        self.username = username
        self.email = email
        self.password = password
        self.phone_number = '+19857188538'

    def __repr__(self):
        return '<User {0}, Email {1}, Password {2}>'.format(self.username, self.email, self.password)


#-------------------------------------------------------------------------------
# Controllers
#-------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # TODO: error messages

    if request.method == 'POST':
        # TODO: check username
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None:
        # Later: check passwords
            session['logged_in'] = True
            return redirect(url_for('student'))

    return render_template('login.html')

@app.route('/my_student', methods = ['GET'])
def student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # TODO: render student template
    return 'Student Page.'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect(url_for('login'))

@app.route('/student/home')
def student():
    return render_template('student.html')

@app.route('/student/help')
def help():
    return render_template('help.html')

@app.route('/student/forms')
def forms():
    return render_template('forms.html')

@app.route('/register')
def register():
    return render_template('register.html')


#
# SMS
#

@app.route('/SMSResponse')
def hello_monkey():
    resp = twillio.twiml.Response()
    resp.sms("Hello, Mobile DOG!!!")
 

#-------------------------------------------------------------------------------
# Database Changes
#-------------------------------------------------------------------------------

@app.route('/register_user', methods = ['POST'])
def add_user():

    user = User(request.form['username'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('student'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
