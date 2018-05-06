import schedule
import datetime
import smtplib
import glob
import errno
import json
import os.path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config.ps import ps
import csv
from config.common import ORDER_FIELDS

path_to_order_files = '../frontend/order_files/'
path_to_send_to_chef_files = 'send_to_chef_files/'
sender_email_address = 'LttsLunch@gmail.com'
sender_email_password = ps
receiver_email_address = 'davw664@gmail.com'

# Add the field notes to the end of the list
fields = ORDER_FIELDS
fields.append('notes')


def set_order():
    path = os.path.join(path_to_order_files, '*.json')
    files = glob.glob(path)
    with open(os.path.join(path_to_send_to_chef_files, 'order_lunch_' + str(datetime.date.today())) + '.csv',
              'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()

        for name in files:
            try:
                with open(name, encoding='utf-8') as f:
                    writer.writerow(dict(json.load(f)))

            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise


def empty_orders_dir():
    """
    Delete all json files from the 'order_files' file
    :return:
    """
    path = os.path.join(path_to_order_files, '*.json')
    files = glob.glob(path)
    for name in files:
        os.remove(name)


def send_email():
    """
    Send email to the chef
    :return:
    """
    email_subject_line = 'Please read the email!'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Good morning Amit!!' + '\n\n' + "This is an automatic email send to you!!"
    email_body += '\n\n' + "Have A wonderful day!!" + '\n\n' + "David"
    msg.attach(MIMEText(email_body, 'plain'))

    filename = os.path.join(path_to_send_to_chef_files,
                            'order_lunch_' + str(datetime.date.today())) + '.csv'
    part = MIMEBase('application', 'octet-stream')
    with open(filename, 'rb') as attachment_file:
        part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment_file; filename = order_lunch_" +
                        str(datetime.date.today()) + '.csv')

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
    empty_orders_dir()
    # schedule.every().day.at("10:45").do(set_order)
    # schedule.every().day.at("11:46").do(send_email)
    # schedule.every().day.at("11:57").do(empty_orders_dir)
    #
    # schedule.every(2).minutes.do(set_order)
    #
    while True:
        schedule.run_pending()
