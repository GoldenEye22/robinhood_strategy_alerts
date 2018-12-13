# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:51:18 2018

@author: Andy
"""
import smtplib
#send an email update (or text message)  
def send_email(emailstr,msg,sub):
    emailstr = open('@usrpw.txt','r').read().split(',')
    gmail_user = emailstr[0]
    gmail_pwd  = emailstr[1]
    email1     = emailstr[2]
    email2     = emailstr[3]
    FROM       = emailstr[4]
    TO = [email1,email2] #must be a list
    SUBJECT = []
    SUBJECT.append('Robinhood Trade Alert ----- RealTime')
    SUBJECT.append('Robinhood Current Portfolio Weight %')
    SUBJECT.append('Robinhood Trade Timeline --- Nightly')
    TEXT = msg

    # Prepare actual message
    message = '''\From: %s\nTo: %s\nSubject: %s\n\n%s
    ''' % (FROM, ', '.join(TO), SUBJECT[sub], TEXT)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'Successfully Sent Stock Alert'
    except:
        print 'Failed to Send Stock Alert'
    return