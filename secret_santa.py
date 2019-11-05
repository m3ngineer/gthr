''' Pulls names for Secret Santa! '''

import random
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import secret_santa_config

def send_email(from_, to_, username, password, subject, body):

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, password)
        print('Logged into server..')

        msg = MIMEMultipart()
        msg["From"] = from_
        msg["To"] = to_
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'html'))

        server.sendmail(from_, to_, msg.as_string())
        server.quit()

def pull_names(secret_santa_config_file):
    '''
    secret_santa_config_file: path to file that contains names, emails, and a list of
    pairs that should not be matched
    '''

    gifter_names = list(secret_santa_config_file.names.keys())
    receiver_names = list(secret_santa_config_file.names.keys())

    subject = 'Your Eng Family Secret Santa name is here!'

    while gifter_names:
        gifter = random.choice(gifter_names)
        receiver = random.choice(receiver_names)

        if gifter != receiver and set([gifter,receiver]) not in secret_santa_config_file.invalid_matches:
            receiver_names.remove(receiver)
            gifter_names.remove(gifter)

            msg = '''Janet here!
                    <p>Hi {}, your secret santa person for this year is {}!</p>

                    <p>If this doesn't look correct, please reply to this email letting
                    me know and we'll repick names.</p>

                    <p>Love,<br>
                    Janet</p>
                    '''.format(gifter, receiver)
            recipient_email = secret_santa_config_file.names[gifter]
            send_email(from_=secret_santa_config_file.email['username'],
                to_=secret_santa_config_file.email['username'],
                username=secret_santa_config_file.email['username'],
                password=secret_santa_config_file.email['password'],
                subject=subject, body=msg)

    print('Emails sent.')
    return

if __name__ == "__main__":

    pull_names(secret_santa_config)
