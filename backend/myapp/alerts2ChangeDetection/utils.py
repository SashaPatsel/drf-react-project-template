import json
import os
import sys
from stat import *
import requests
from requests.auth import HTTPBasicAuth
import logging
import time
import subprocess
import config
from functools import partial # needed to pass multiple variables to thread_pool.map
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException

def send_email():
    user = 'data@skytruth.org'
    pwd = 'tRmWsf6YGHtT6G6j'
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = 'daniel.cogswell@skytruth.org'
    SUBJECT = 'New planet.com image'
    TEXT = 'here it is'

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

def __convert_json_to_text(jsongeom):
    #print ("jsongeom:" + jsongeom)
    if "[[[" in jsongeom:
        textgeom = 'POLYGON((' + jsongeom[jsongeom.find('[[[') + 2:jsongeom.find(']]]')] + '))'
    else:
        textgeom = 'POLYGON((' + jsongeom[jsongeom.find('[[') + 2:jsongeom.find(']]')] + '))'
    textgeom = textgeom.replace('],', 'xxxx')
    textgeom = textgeom.replace('[', ' ')
    textgeom = textgeom.replace(',', ' ')
    textgeom = textgeom.replace('xxxx', ',')
    #print ("textgeom:" + textgeom)
    return textgeom

def email_error(error_msg):
    user = 'data@skytruth.org'
    pwd = 'tRmWsf6YGHtT6G6j'
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = 'daniel.cogswell@skytruth.org'
    SUBJECT = 'Error found'
    TEXT = error_msg

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

