from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def hello_you_there():
  resp = twilio.twiml.Response()
  resp.sms("hello, you there?!")
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)