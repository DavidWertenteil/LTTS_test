import schedule
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email():
    sender_email_address = 'david.wertenteil@lnttechservices.com'
    sender_email_password = ''
    receiver_email_address = 'Amit.Tene@lnttechservices.com'

    email_subject_line = 'Please read the email!'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Good morning Amit!!' + '\n\n' + "This is an automatic email send to you!!"
    email_body += '\n\n' + "Have A wonderful day!!" + '\n\n' + "David"
    msg.attach(MIMEText(email_body, 'plain'))

    filename = 'text.txt'
    attachment_file = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment_file).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment_file; filename = " + filename)

    msg.attach(part)

    email_body_content = msg.as_string()
    server = smtplib.SMTP('smtp-mail.outlook.com:587')
    server.starttls()
    server.login(sender_email_address, sender_email_password)
    server.sendmail(sender_email_address, receiver_email_address, email_body_content)
    server.quit()


if __name__ == '__main__':
    schedule.every().day.at("08:30").do(send_email)
    while True:
        schedule.run_pending()
