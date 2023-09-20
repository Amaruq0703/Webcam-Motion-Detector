import smtplib
import ssl
import os
import imghdr
from email.message import EmailMessage

def send_email(imgpath):
    print('Send email func started')
    message = EmailMessage()
    message['Subject'] = 'Camera detected an object'
    message.set_content('We detected an object in your camera')
    
    with open(imgpath, 'rb') as file:
        content = file.read()
        message.add_attachment(content, maintype = 'image',
                               subtype = imghdr.what(None, content) )





    host = 'smtp.gmail.com'
    port = 587

    username = 'aditya.khera7@gmail.com'
    password = os.getenv('PASSWORD')
    receiver = 'aditya.khera7@gmail.com'

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)
    gmail.sendmail(username, receiver, message.as_string())
    gmail.quit()

    print('Send email func ended')
    