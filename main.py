import schedule
import time
import smtplib, ssl
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json
import random


# function that receives the data of sent email and saves on the Email_History.json file
def saveEmailRecord(emailData):
    while True:
        # load the json file for logging email history, if it does not exist create it
        try:
            with open("Email_History.json", "r") as file:
                email_history = json.load(file)
        except:
            email_history = {}
        email_id = str((round(random.random() * 10000000000)))
        if "email" + email_id not in email_history:
            emailRecord = emailData
            email_history["email" + str(email_id)] = emailRecord
            with open("Email_History.json", "w") as file:
                json.dump(email_history, file)
            break

# this function will be called based on the scheduled time
def job():

    sender = 'testsenderaccount@gmail.com'
    password = 'eqnmuzsgcqzaepmt'
    receivers = ["test@mailinator.com", "emailtest@mailinator.com", "testemailautomation@mailinator.com"]

    context = ssl.create_default_context()

    try:
        # connect to email server (gmail in this case)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender, password)
                for receiver in receivers:
                    # compose the email
                    text = 'Hello ' + receiver + ", here are your daily reports for today. "
                    msg = MIMEMultipart(text)
                    msg['Subject'] = 'Daily reports for ' + receiver
                    msg['From'] = sender
                    msg['To'] = receiver

                    # attach the attachment to the email
                    dailyreport = 'DailyReport.txt'
                    with open(dailyreport, 'r') as f:
                        part = MIMEApplication(f.read(), Name=basename(dailyreport))
                    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(dailyreport))
                    msg.attach(part)

                    # send the email
                    server.sendmail(sender, receiver, msg.as_string())
                    print("Successfully sent email to " + receiver)

                    # crating the object with the email data
                    emailRecord = {
                        "sender": sender,
                        "receiver": receiver,
                        "subject": msg['Subject'],
                        "text": text,
                        "attachment": dailyreport
                    }
                    saveEmailRecord(emailRecord)

            except:
                print("An error occurred while signing in or your credentials are wrong...")
                emailRecord = {
                    "errorMessaage": "There was a problem while signing in to your email"
                }
                saveEmailRecord(emailRecord)
    except:
        print("An error occurred while connecting to the server...")
        emailRecord = {
            "errorMessage": "There was a problem while connecting to server"
        }
        saveEmailRecord(emailRecord)

# setting a schedule to run the script
schedule.every().day.at("10:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)