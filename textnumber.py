# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import transitland
# Set environment variables for your credentials
# Read more piat http://twil.io/secure
account_sid = "ACc6c4d9ab8bd0382450b9e5904e044ca4"
auth_token = "44e94608d453e4fa24e403fd128ba7ea"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body=transitland.body,
  from_="+15676777869",
  to=transitland.phone_number
)
print(message.sid)