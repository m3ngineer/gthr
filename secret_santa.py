''' Pulls names for Secret Santa! '''

import random
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
from collections import Counter

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

    # Choose secret santa pairs
    restart = True
    while restart:
        gifter_names = list(secret_santa_config_file.names.keys())
        receiver_names = list(secret_santa_config_file.names.keys())
        pairs = []

        for gifter in gifter_names:
            restart = False
            check_pairing = True
            while check_pairing:
                receiver = random.choice(receiver_names)
                if gifter != receiver and set([gifter,receiver]) not in secret_santa_config_file.invalid_matches:
                    receiver_names.remove(receiver)
                    pairs.append((gifter, receiver))
                    check_pairing = False
                elif len(receiver_names) == 1: # if only person left has themselves to pick
                    # Start over
                    restart = True
                    check_pairing = False
                elif (len(receiver_names) == 2) and (set(receiver_names) in secret_santa_config_file.invalid_matches):
                    # Only remaining names cannot be matched
                    # Start over
                    restart = True
                    check_pairing = False
                else:
                    continue

    # Check pairs
    check_pairs = Counter([j for i in [list(pair) for pair in pairs] for j in i]).values()
    pair_warning = any([False if i <= 2 else True for i in check_pairs])
    multiple_names_warning1 = sorted(secret_santa_config.names.keys()) != sorted([i[0] for i in pairs])
    multiple_names_warning2 = sorted(secret_santa_config.names.keys()) != sorted([i[1] for i in pairs])
    if pair_warning:
        print('Repick names!!')

    elif multiple_names_warning1 or multiple_names_warning2:
        print('Repick names!!')

    else:
        # Send emails
        subject = 'The 2022 Virtual Holiday Cookie Bake-off!'

        for pair in pairs:
            gifter = pair[0]
            receiver = pair[1]

            file = open('secret_santa_msg.html', 'r')
            msg = file.read()
            msg = msg.format(gifter, receiver)

            gifter_email = secret_santa_config_file.names[gifter]
            send_email(from_=secret_santa_config_file.email['username'],
                to_=gifter_email,
                username=secret_santa_config_file.email['username'],
                password=secret_santa_config_file.email['password'],
                subject=subject, body=msg)

        print('Emails sent.')

    return

if __name__ == "__main__":

    pull_names(secret_santa_config)
