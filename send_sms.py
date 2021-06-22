from twilio.rest import Client
import os

# Your Account SID from twilio.com/console
account_sid = os.environ['ACCOUNT_SID']
# Your Auth Token from twilio.com/console
auth_token  = os.environ['AUTH_TOKEN']

client = Client(account_sid, auth_token)

message = client.messages.create(
    to=os.environ['MY_PHONE_NUMBER'], 
    from_=os.environ['FROM_PHONE_NUMBER'],
    body="Hello, from PanTrack!!")

print(message.sid)