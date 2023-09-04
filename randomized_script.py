import smtplib
import pygsheets
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import random
from google.oauth2.credentials import Credentials
import os
import pandas as pd

client_secret_json = os.environ['CLIENT_SECRET_JSON']
token_json = os.environ['TOKEN_JSON']

gc = pygsheets.authorize(client_secret=client_secret_json)


sh = gc.open('Randomized Reach Out')
wks = sh.sheet1
data = wks.get_all_values()
headers = data.pop(0)

df = pd.DataFrame(data, columns=headers)
weights = {
    'Low': 0.2,    # Lower probability for 'low' frequency
    'Medium': 0.4, # Medium probability for 'medium' frequency
    'High': 0.6    # Higher probability for 'high' frequency
}

random_row = df.sample(1, weights=df['Frequency'].map(weights))
name_person = random_row['Name'].iloc[0]
contact_person = random_row['Contact Method'].iloc[0]

creds_filename = 'token.json'
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
if not os.path.exists(creds_filename):
	flow = Credentials.from_authorized_user_info(token_json, SCOPES)
	creds = flow.run_local_server(port=0)
	with open(creds_filename, 'w') as token:
		token.write(creds.to_json())
else:
	creds = Credentials.from_authorized_user_file(creds_filename, SCOPES)

service = build('gmail', 'v1', credentials=creds)
message = MIMEText("Remember to contact " + str(name_person) + ' using ' + str(contact_person))
message['to'] = 'deabardhoshi45@gmail.com'
message['subject'] = 'Your Weekly Reach Out Nudge'
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None

