import os
from flask import Flask

# quickstart database
from flask.ext.sqlalchemy import SQLAlchemy

#-------------------------------------------------------------------------------
# Initialization
#-------------------------------------------------------------------------------

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config.update( DEBUG = True )

# contains functions/helpers form sqlalchemy and sqlalchmey.orm
db = SQLAlchemy(app)

# TODO: double check what this does
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
        return '<User %r>' % self.password


#-------------------------------------------------------------------------------
# Controllers
#-------------------------------------------------------------------------------

# Public

@app.route('/')
def index():
    return 'Single Stop.'


#-------------------------------------------------------------------------------
# Post Requests
#-------------------------------------------------------------------------------

@app.route('/add_user', methods = ['POST'])
def add_user():
    # handle request user

    # create user object (user = ...)

    # add user to database

    # commit changes

    return

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
