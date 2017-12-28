# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: function.py

import os
import pyodbc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

class mail():

    def __init__(self, smtp_server, user=None, pwd=None):
        self.smtp_server = smtp_server
        self.user = user
        self.pwd = pwd
        postfix = smtp_server.split('.')
        self.sender = 'chengjie_jack@126.com'

    def send_mail(self, mail_tolist, body, subject, *attachment):
        '''
        Send mail
        :param mail_tolist: a string, use , to divide multiple addres
        :param body: The text displayed in mail
        :param subject: subject of the mail
        :param attachment: attachments' path
        :return: 
        '''

        try:
            if len(attachment):
                msg = MIMEMultipart()
                body = MIMEText(body, _subtype='plain', _charset='utf-8')
                msg.attach(body)
                for i in xrange (0,len(attachment)):
                    att = MIMEText(open(attachment[i], 'rb').read(), 'base64', 'utf-8')
                    att['Content-Type'] = 'application/octet-stream'
                    att['Content-Disposition'] = 'attachment; filename=" ' + attachment[i].split('/')[-1] + '"'
                    msg.attach(att)
            else:
                msg = MIMEText(body, _subtype='plain', _charset='utf-8')

            msg['to'] = mail_tolist
            msg['from'] = self.sender
            msg['subject'] = subject

            smpt = smtplib.SMTP(self.smtp_server)
            if self.user:
                smpt.login(self.user, self.pwd)
            smpt.sendmail(self.sender, mail_tolist, msg.as_string())
            print 'mail is sent'

        except Exception,e:
            print e

        finally:
            smpt.close()

class sql():

    def __init__(self, driver,server,database,uid,pwd):
        self.conn_str = 'driver={'+ driver + '};server=' + server + ';database=' + database + ';uid=' + uid + ';pwd=' + pwd

    def query(self,sqlstatement, *param):
        '''
        Run the select statement on the target database server
        :param sqlstatement: the select statement, the serach condition in where clause can be replaced by ? to be more flexiable
        :param param: a list of values to fill in ? in where clause
        :return: A list of all the rows in the query. Use row[rownumber].[columnname] to get a specific cell value. otherwise,
                use row[rownumber] to get a list of the specific row values.
        '''

        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            rows = cursor.execute(sqlstatement, *param).fetchall()
        return rows

    def execute(self,sqlstatement, *param):
        '''
        Run insert, update, delete and stored procedures
        :param sqlstatement: 
        :param param: 
        :return: 
        '''

        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            count = cursor.execute(sqlstatement, *param).rowcount
            conn.commit()
        return count

if __name__ == '__main__':
    file_path = r'C:\AutoResults\results.txt'
    file_path2 = r'C:\AutoResults\results2.txt'
    mailInstance = mail('smtp.126.com','chengjie_jack','Eric890420WY')
    mailInstance.send_mail('jack.cheng@highjump.com', 'testresult', 'csd project', file_path, file_path2)
    # sql = sql('SQL Server Native Client 11.0', 'SCA08SX64S12', 'AAD', 'sa', 'HJSPASS#1')
    # results = sql.query("select * from t_employee where id = ?", 'AMY')
    # for result in results:
    #     print result
    # rowcount = sql.execute('update t_employee set password=? where id=?', 'AMY1', 'AMY')
    # print rowcount
