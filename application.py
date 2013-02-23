import os
from flask import Flask, request, session, url_for, render_template, redirect

# quickstart database
from flask.ext.sqlalchemy import SQLAlchemy

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'something secret'
app.config.update( DEBUG = True )

# contains functions/helpers form sqlalchemy and sqlalchmey.orm
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

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0}, Email {1}, Password {2}>'.format(self.username, self.email, self.password)


#-------------------------------------------------------------------------------
# Controllers
#-------------------------------------------------------------------------------

@app.route('/')
def index():
    return 'Single Stop.'

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

@app.route('/student', methods = ['GET'])
def student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # TODO: render student template
    return 'Student Page.'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect(url_for('login'))
    

#-------------------------------------------------------------------------------
# Database Changes
#-------------------------------------------------------------------------------

@app.route('/register_user', methods = ['POST'])
def add_user():
    # handle request

    # create user object (user = ...)

    # add user to database

    # commit changes

    return

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
