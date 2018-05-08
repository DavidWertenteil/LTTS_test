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
import config.common as conf

path_to_order_files = 'frontend/order_files/'
path_to_send_to_chef_files = 'backend/send_to_chef_files/'
sender_email_address = 'LttsLunch@gmail.com'
sender_email_password = ps
receiver_email_address = conf.RECEIVER_EMAIL_ADDRESS

# Add the field notes to the end of the list
fields = conf.ORDER_FIELDS
fields.append('notes')


def set_order():
    path = os.path.join(path_to_order_files, '*.json')
    files = glob.glob(path)
    try:
        with open(os.path.join(path_to_send_to_chef_files, 'order_lunch_' + str(datetime.date.today())) + '.csv',
                  'w+', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fields)
            writer.writeheader()

            for name in files:
                try:
                    with open(name, encoding='utf-8') as f:
                        writer.writerow(dict(json.load(f)))
                except IOError as exc:
                    if exc.errno != errno.EISDIR:
                        raise
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

    # Now that the csv is ready send the email
    send_email()


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
    email_subject_line = str(datetime.date.today()) + 'הזמנה לתאריך - '
    email_body = "הזמנת אוכל"
    filename = os.path.join(path_to_send_to_chef_files,
                            'order_lunch_' + str(datetime.date.today())) + '.csv'
    for email_address in receiver_email_address:
        msg = MIMEMultipart()
        msg['From'] = sender_email_address
        msg['To'] = email_address
        msg['Subject'] = email_subject_line

        msg.attach(MIMEText(email_body, 'plain'))

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

    # Now that the email was send we can delete all json files
    empty_orders_dir()


if __name__ == '__main__':
    # schedule.every().day.at(conf.ORDER_TIME).do(set_order)
    
    while True:
        schedule.run_pending()
