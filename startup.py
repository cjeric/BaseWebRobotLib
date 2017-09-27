import robot
from selenium import webdriver
import os

command = r'python -m robot --variablefile C:\Users\jackc\PycharmProjects\robot\variables.py C:\RobotTestCase\TestSuite1.robot'
# command = r'python -m robot C:\Users\jackc\Desktop\scripts\test\Suite2-10.robot'
p = os.popen(command)
print p.read()
