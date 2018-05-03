import schedule
import datetime
import smtplib
import glob
import errno
import json
import os.path
from pprint import pprint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from ps import ps

path_to_order_files = 'order_files/'
path_to_send_to_chef_files = 'send_to_chef_files/'


def set_order():
    path = os.path.join(path_to_order_files, '*.json')
    files = glob.glob(path)
    order_data = {}
    for name in files:
        try:
            with open(name, encoding='utf-8') as f:
                order_data.update(json.load(f))

        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise  # Propagate other kinds of IOError.

    with open(os.path.join(path_to_send_to_chef_files, 'order_lunch_' + str(datetime.date.today())) + '.json',
              'w') as outfile:
        json.dump(order_data, outfile)


def empty_orders_dir():
    path = os.path.join(path_to_order_files, '*.json')
    files = glob.glob(path)
    for name in files:
        os.remove(name)


def send_email():
    sender_email_address = 'LttsLunch@gmail.com'
    sender_email_password = ps
    receiver_email_address = 'davw664@gmail.com'

    email_subject_line = 'Please read the email!'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Good morning Amit!!' + '\n\n' + "This is an automatic email send to you!!"
    email_body += '\n\n' + "Have A wonderful day!!" + '\n\n' + "David"
    msg.attach(MIMEText(email_body, 'plain'))

    filename = os.path.join(path_to_send_to_chef_files,
                            'order_lunch_' + str(datetime.date.today())) + '.json'
    attachment_file = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment_file; filename = order_lunch_" +
                    str(datetime.date.today()) + '.json')
    msg.attach(part)

    email_body_content = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email_address, sender_email_password)
    server.sendmail(sender_email_address, receiver_email_address, email_body_content)
    server.quit()


if __name__ == '__main__':
    set_order()
    send_email()
    # empty_orders_dir()
    # schedule.every().day.at("10:52").do(set_order)
    # schedule.every().day.at("10:53").do(send_email)
    # while True:
    #     schedule.run_pending()
