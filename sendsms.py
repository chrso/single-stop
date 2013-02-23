from twilio.rest import TwilioRestClient

account_sid = "AC529852db190279bf7ed541ae7340fd4a"
auth_token = "8953ef895b2a097f71a4e3e7937ced28"
client = TwilioRestClient(account_sid,auth_token);

message = client.sms.messages.create(body="Jenny please?! i love u",
  to="+19857188538",
  from_="+19857180534")
print message.sid