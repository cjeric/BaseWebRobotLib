# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: function.py

from selenium import webdriver
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class mail():

    def __init__(self, user, pw, smtp_server):
        self.smtp_server = smtp_server
        self.user = user
        self.pw = pw
        postfix = smtp_server.split('.')
        self.sender = user + '@' + postfix[-2] + '.' + postfix[-1]

    def send_mail(self, mail_tolist, body, subject, attachment = None):
        try:
            if attachment == None:
                msg = MIMEText(body, _subtype='plain', _charset='utf-8')
            else:
                msg = MIMEMultipart()
                body = MIMEText(body, _subtype='plain', _charset='utf-8')
                msg.attach(body)

                att1 = MIMEText(open(attachment,'rb').read(), 'base64', 'utf-8')
                att1['Content-Type'] = 'application/octet-stream'
                att1['Conent-Disposition'] = 'attachment; filename="log2.txt" ' #+ attachment.split('/')[-1]
                msg.attach(att1)

            msg['to'] = mail_tolist
            msg['from'] = self.sender
            msg['subject'] = subject

            smpt = smtplib.SMTP(self.smtp_server)
            smpt.login(self.user, self.pw)
            smpt.sendmail(self.sender, mail_tolist, msg.as_string())

        except Exception,e:
            print e

        finally:
            smpt.close()

if __name__ == '__main__':
    file_path = r'C:\AutoResults\results.txt'
    mailInstance = mail('chengjie_jack', 'Eric890420WY', 'smtp.126.com')
    mailInstance.send_mail('jack.cheng@highjump.com', 'testresult', 'csd project', file_path)