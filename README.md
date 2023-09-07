# Randomized Reach Out Nudger

## Motivation:

I wanted to make this project mostly as an automated tool to nudge me to keep in contact with people I've met. Friends and extended family, co-workers or people I've struck up a conversation with at various events. It is often hard to maintain relationships, especially over long distances or over time so this tool is my approach to cultivating more meaningful, deeper relationships with people.
Essentially, it consists of a spreasheet, in which you write up folks you want to be reminded to stay in touch with as well a section for various anniversaries coming up. Read below for how to set it up, make a list of contacts, schedule an email and have your own little nudge to forge better relationships.

## Set-up:

1. Spreadsheet:
   - Make a Google Sheets spreadsheet called "Randomized Reach Out" with two sheets (sheet1 and sheet2). Sheet1 has three columns: "Name", "Contact Method" and "Frequency". Frequency is low, medium, high depending on how often you want to be reminded to send a message to a specific person. Start populating it with people you know! Sheet2 also has three columns: "Person", "Anniversary" (date of occassion), "Type" (what they are celebrating). Populate this too.
2. API credentials:
   - You need to set up API credentials for both the Google Sheets and the email integrations. Follow this tutorial for a guide on the Google Sheets credentials: https://pygsheets.readthedocs.io/en/stable/authorization.html. Follow this for email credentials: https://mailtrap.io/blog/python-send-email-gmail/
3. Make a few replacements:
   - Replace your own email, path to client_secret, creds_filename and optionally the set of weights for the frequency column of sheet1.
4. Set up cron job:
   - To automate sending this email to yourself, set up cron jobs that run the file periodically at your desired frequency. A simple tutorial on doing this: https://betterprogramming.pub/how-to-execute-a-cron-job-on-mac-with-crontab-b2decf2968eb
  
Enjoy!

P.S. Let me know if you have any issues or suggestions!
