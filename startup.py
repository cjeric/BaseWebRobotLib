# _*_ coding: utf-8 _*_
#!c:/Python27
#Filename: startup.py

from subprocess import Popen,PIPE
from CommonFunction import mail

result_dir = r'--outputdir C:\AutoResults'
testcases_dir = r'C:\BaseWebRobotLib\RobotTestCase\test.txt'

logfile_path = result_dir.split(' ')[1] + r'\log.html'
reportfile_path = result_dir.split(' ')[1] + r'\report.html'
outputfile_path = result_dir.split(' ')[1] + r'\output.xml'
user = 'chengjie_jack'
pwd = 'Eric890420WY'
smtp_server = 'smtp.126.com'
mailtolist = 'jack.cheng@highjump.com'


def run(command):
    result = Popen(command, shell=True,stdin=PIPE,stdout=PIPE, stderr=PIPE)
    result.wait()
    stdout, stderr = result.communicate()
    return result, stdout, stderr



if __name__ == '__main__':
    command = 'robot ' + result_dir + ' ' + testcases_dir
    #result = run(command)
    result,stdout,stderr=run(command)
    email = mail(smtp_server,user,pwd)
    email.send_mail(mailtolist, 'testresult', 'robot project', logfile_path)
    print stdout


