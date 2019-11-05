''' Pulls names for Secret Santa! '''

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import secret_santa_config

def send_email(from_, to_, username, password, subject, body):

    print('-1')
    msg = MIMEMultipart()
    msg["From"] = from_
    msg["To"] = to_
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'html'))

    print('0')
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    print('1')
    server.ehlo()
    print('2')
    server.login(username, password)
    print('3')
    server.sendmail(from_, to_, msg.as_string())
    print('4')
    server.quit()

def pull_names(secret_santa_config_file):
    '''
    secret_santa_config_file: path to file that contains names, emails, and a list of
    pairs that should not be matched
    '''

    gifter_names = list(secret_santa_config_file.names.keys())
    receiver_names = list(secret_santa_config_file.names.keys())

    while gifter_names:
        gifter = random.choice(gifter_names)
        receiver = random.choice(receiver_names)
        if gifter != receiver and set([gifter,receiver]) not in secret_santa_config_file.invalid_matches:
            print(gifter, receiver)
            receiver_names.remove(receiver)
            gifter_names.remove(gifter)

        # send email
    return



if __name__ == "__main__":

    pull_names(secret_santa_config)
    send_email(secret_santa_config.email['username'], secret_santa_config.email['username'],
        secret_santa_config.email['username'], secret_santa_config.email['password'], 'test', 'testing')
