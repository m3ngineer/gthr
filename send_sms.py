# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.environ['twilio_account_sid']
auth_token = os.environ['twilio_auth_token']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hey this is your friendly neighborhood bot, Janet!",
                     from_='+19143369499',
                     to='+15748498881'
                 )

print(message.sid)
