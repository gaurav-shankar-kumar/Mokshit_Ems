

from ast import Return
from cgitb import html
from email import message_from_binary_file
from pyexpat.errors import messages
import re
from urllib import request
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# email = EmailMessage(
#     'Hello',
#     'Body goes here',
#     'from@example.com',
#     ['to1@example.com', 'to2@example.com'],
#     ['bcc@example.com'],
#     reply_to=['another@example.com'],
#     headers={'Message-ID': 'foo'},
# )

def Welcomemail(email,password,name):
    subject = 'Your Login Credentials'
    template = "mokshitsite/mail_template.html"
    message = render_to_string(template,{'name':name,'email':email ,'password':password})
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    email = EmailMessage(subject,message,email_from,recipient_list)
    email.content_subtype = 'html'
    email.send()
    return True


# Welcomemail('mahipuja786@gmail.com','12345','pooja')

