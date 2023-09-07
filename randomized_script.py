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
from dateutil.parser import parse
from datetime import datetime, timedelta
from jinja2 import Template





gc = pygsheets.authorize(client_secret='client_secret.json')


sh = gc.open('Randomized Reach Out')



wks = sh.sheet1
wks2 = sh.worksheet_by_title('Sheet2')
data = wks.get_all_values()
data2 = wks2.get_all_values()
headers = data.pop(0)
headers2 = data2.pop(0)

df = pd.DataFrame(data, columns=headers)
weights = {
    'Low': 0.2,    # Lower probability for 'low' frequency
    'Medium': 0.4, # Medium probability for 'medium' frequency
    'High': 0.6    # Higher probability for 'high' frequency
}

random_row = df.sample(1, weights=df['Frequency'].map(weights))
name_person = random_row['Name'].iloc[0]
contact_person = random_row['Contact Method'].iloc[0]

df2 = pd.DataFrame(data2, columns=headers2)
df2 = df2.dropna()
dates_anniversaries =  df2['Anniversary'].map(lambda x: parse(x + '2023'))
df2['Anniversary'] = dates_anniversaries
today = datetime.now().date()
one_week_from_today = today + timedelta(days=7)

# checking if any anniversaries:
df2['Anniversary_ThisWeek'] = df2['Anniversary'].map(lambda x: today <= x <= one_week_from_today)
unique_anniversary_names = df2[df2['Anniversary_ThisWeek']]['Person'].unique()
anniversary_rows = df2[df2['Anniversary_ThisWeek']]['Person'].unique()
anniversary_html = "Also: <br>"
for name in unique_anniversary_names:
    # Find the rows where 'person' matches the current name
    matching_rows = df2[df2['Person'] == name]
    
    # Loop through the matching rows (if there are multiple anniversaries for the same person)
    for index, row in matching_rows.iterrows():
        anniversary_date = row['Anniversary']
        anniversary_type = row['Type']
        person_name = row['Person']
        if not row['Person'] == '':
            anniversary_html += f"<p><strong>{person_name}</strong> has a <strong>{anniversary_type}</strong> this week! on <strong>{anniversary_date}</strong></p>"

creds_filename = 'token.json'
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
if not os.path.exists(creds_filename):
	flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
	creds = flow.run_local_server(port=0)
	with open(creds_filename, 'w') as token:
		token.write(creds.to_json())
else:
	creds = Credentials.from_authorized_user_file(creds_filename, SCOPES)


html = f"""\
<html>
<head>
    <meta charset="UTF-8">
    <title>Your Weekly Reach Out Nudge</title>
  </head>
<body>
    <div class="container">
        <h1>Your Weekly Reach Out Nudge</h1>
        <p>Hi there!</p>
        <p>I just wanted to remind you to reach out to:</p>
        <p><strong>{name_person}</strong> using <strong>{contact_person}</strong></p>

        {anniversary_html}


        <p>Don't forget to stay in touch!</p>
        <p>Best regards,</p>
        <p>Automated Dea</p>


    </div>
</body>
</html>
"""

service = build('gmail', 'v1', credentials=creds)
message = MIMEText(html, 'html', 'utf-8')
message['to'] = 'deabardhoshi45@gmail.com'
message['subject'] = 'Your Weekly Reach Out Nudge'
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None



