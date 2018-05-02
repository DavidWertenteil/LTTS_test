import schedule
import time

# def job():
#     print("I'm working...")

# schedule.every(10).minutes.do(job)
# schedule.every(0.5).minutes.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
# Import smtplib for the actual sending function


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def main():
    sender_email_address = 'david.wertenteil@lnttechservices.com'
    sender_email_password = ''
    receiver_email_address = 'david.wertenteil@lnttechservices.com'

    email_subject_line = 'Test!'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Hello World. This is Python email sender application with Attachments.'
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
    main()
