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
if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.config['SECRET_KEY'] = 'something secret'
app.config.update( DEBUG = True )

# contains functions/helpers form sqlalchemy and sqlalchemy.orm
db = SQLAlchemy(app)

# migrate database -- doesn't overwrite tables
db.create_all()


#Provide interface to connect with potential Single Stop Org database 
app.config['SQLALCHEMY_BINDS'] = {
    'singleStopOrg':      'sqlite:////tmp/some.db'
}
db.create_all(bind = ['singleStopOrg'])




# stuff need by twillio to send messages
account_sid = "AC529852db190279bf7ed541ae7340fd4a"
auth_token = "8953ef895b2a097f71a4e3e7937ced28"
client = TwilioRestClient(account_sid,auth_token);

#-------------------------------------------------------------------------------
# Models
#-------------------------------------------------------------------------------

# declarative modelling
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(25))
    phone_number = db.Column(db.String(12))
    wants_texts = db.Column(db.String(10))

    def __init__(self, username, email, password, phone_number):

        # TODO: figure out how to validate input

        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.wants_texts = 'maybe'

    def __repr__(self):
        return '<User {0}, Email {1}, Password {2}>'.format(self.username, self.email, self.password)


#Provide interface to connect with potential Single Stop Org database 
class Benefit(db.Model):
    __bind_key__ = 'singleStopOrg'
    id = db.Column(db.Integer, primary_key=True)
    benefitType = db.Column(db.String(20), unique=True)
    benefitAmount = db.Column(db.String(10), unique=True)
    school = db.Column(db.String(30), unique=True)
    location = db.Column(db.String(50), unique=True)        #office location to get the benfit
    documentName = db.Column(db.String(30), unique=True)    #document needed for the benfit, might not be one
    
    def __init__(self, benefitType, benefitAmount, school, location, documentName):
        self.benefitType = benefitType
        self.benefitAmount = benefitAmount
        self.school = school
        self.location = location
        self.documentName = documentName
        
    def __repr__(self):
        return '<User {0}, Email {1}>'.format(self.benefitType, self.benefitAmount)



#-------------------------------------------------------------------------------
# Controllers
#-------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get("logged_in"):
        return redirect(url_for('student'))

    # TODO: error messages

    if request.method == 'POST':
        # TODO: check username
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None:
        # Later: check passwords
            session['logged_in'] = True
            return redirect(url_for('student'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect(url_for('login'))

@app.route('/student')
@app.route('/student/home')
def student():
    if not session.get("logged_in"):
        return redirect(url_for('login'))

    return render_template('student.html')

@app.route('/student/help')
def help():
    if not session.get("logged_in"):
        return redirect(url_for('login'))

    return render_template('help.html')

@app.route('/student/forms')
def forms():
    if not session.get("logged_in"):
        return redirect(url_for('login'))

    return render_template('forms.html')

@app.route('/student/counseling')
def counseling():
    if not session.get("logged_in"):
        return redirect(url_for('login'))

    return render_template('counseling.html')

@app.route('/student/appointment')
def appointment():
    if not session.get("logged_in"):
        return redirect(url_for('login'))

    return render_template('appointment.html')

@app.route('/student/about_us')
def about():
    if not session.get("logged_in"):
        return redirect(url_for('login'))
    
    return render_template('about.html')

@app.route('/register')
def register():
    if session.get("logged_in"):
        return redirect(url_for('student'))

    return render_template('register.html')

#-------------------------------------------------------------------------------
# SMS Notifications API (via Twilio)
#-------------------------------------------------------------------------------

def sendMessage(number,text):
    message = client.sms.messages.create(body=text,
      to=number,
      from_="+19857180534")
    print message.sid
    return 'you cant see me'

@app.route('/SMSResponse', methods=['GET', 'POST'])
def hello_monkey():
    from_number = request.values.get('From')
    response = request.values.get('Body')
    user = User.query.filter_by(phone_number=from_number).first()
    if user is not None:
        if user.wants_texts == 'maybe':
            user.wants_texts = response
            db.session().commit()
            if response == 'yes':
                message = "thanks, you surely wont regret this!"
            else:
                message = "if you ever want reminders, just send us a yes!"
    
    else:
        message = "sorry, we don't recognize that response..."

    message = "u stink"

    resp = twilio.twiml.Response()
    resp.sms(message)
    return str(resp)
 

#-------------------------------------------------------------------------------
# Database Changes
#-------------------------------------------------------------------------------

# can be included in register (potentially)
@app.route('/register_user', methods = ['POST'])
def register_user():

    #TODO: validate input, if not valid, redirect to register page

    user = User(request.form['username'], request.form['email'], request.form['password'], request.form['number'])
    db.session.add(user)
    db.session.commit()
    new_user_text(user.phone_number)

    session['logged_in'] = True 

    return redirect(url_for('student'))

def new_user_text(number):
    text = "Thanks for registering with single-stop. We're here to help you succeed. Want to receive periodic text updates? Reply yes or no."
    sendMessage(number,text)

#-------------------------------------------------------------------------------
# Launcher
#-------------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
