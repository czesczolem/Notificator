import json
import smtplib
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class Notificator:

    def __init__(self):
        '''
        Get connection from Outlook connection
        '''

        self.mail = json.load(open(os.path.abspath('..') + "/mail_secrets.json"),
                              object_pairs_hook=OrderedDict)

        self.conn = smtplib.SMTP(self.mail['SMTPserver'], int(self.mail['SMTPserverPort']))
        self.conn.starttls()
        self.conn.set_debuglevel(False)
        self.conn.login(self.mail['USERNAME'], self.mail['PASSWORD'])

    def reconnect(self):
        print("reconnect...")
        try:
            self.conn.quit()
        except:
            pass

        self.conn = smtplib.SMTP(self.mail['SMTPserver'], int(self.mail['SMTPserverPort']))
        self.conn.starttls()
        self.conn.set_debuglevel(False)
        self.conn.login(self.mail['USERNAME'], self.mail['PASSWORD'])
        self.counter = 0

    def email_generation(self, email_subject, email_text):
        msg = MIMEMultipart('alternative')
        part1 = MIMEText(email_text, 'plain')
        msg.attach(part1)
        tmpmsg = msg
        msg = MIMEMultipart()
        msg.attach(tmpmsg)
        msg['Subject'] = email_subject
        msg['From'] = self.mail['FROM']
        return msg

    def sent_email(self, to_addresses, email_subject, email_text):
        msg = self.email_generation(email_subject, email_text)
        self.conn.sendmail(self.mail['FROM'], to_addresses, msg.as_string())
        print(f"Emails sent to {to_addresses}")

if __name__ == "__main__":
    notificator = Notificator()
    notificator.sent_email(['maciej.tatarek93@gmail.com'], "test email", "test_email")
