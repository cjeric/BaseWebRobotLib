# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: LoginPage.py

from Base import Base
from selenium import webdriver
from selenium.webdriver.common.by import By
from robot.api import logger


class LoginPage(Base):
    url = ''

    #username locator
    username_loc = (By.CSS_SELECTOR, 'hj-textbox[data-hj-test-id="username"]')

    #Function to input username
    def __action_input_username(self, username='Administrator'):
        element = self.find_element(*self.username_loc)
        element.send_keys(username)

    #password_locator
    password_loc = (By.CSS_SELECTOR, 'hj-password-textbox[data-hj-test-id="password"]>input')

    #Function to input password
    def __action_input_password(self, password='HJSPASS'):
        self.find_element(*self.password_loc).send_keys(password)

    #tenant_locator
    tenant_loc = (By.CSS_SELECTOR,'hj-textbox[data-hj-test-id="tenant"]>input' )

    #Function to input tenant
    def __acton_input_tenant(self, tenant ='Tenant'):
        self.find_element(*self.tenant_loc).send_keys(tenant)

    #language locator
    language_dropdown_loc = (By.CSS_SELECTOR,'hj-dropdownlist[data-hj-test-id="language"]>span')
    language_input_loc = (By.CSS_SELECTOR, 'hj-dropdownlist[data-hj-test-id="language"]>span>span>span[class="k-input"]')

    #Function to select language
    def __action_select_language(self, language):
        language_dropdown = self.find_element(*self.language_dropdown_loc)
        language_input = self.find_element(*self.language_input_loc)
        language_dropdown.click()
        language_input.send_keys(language)
        language_dropdown.click()

    #Login button locator
    __login_button_loc = (By.CSS_SELECTOR, 'hj-button[data-hj-test-id="actionButton"]')

    #Function to click Login button
    def __action_click_login(self):
        self.find_element(*self.__login_button_loc).click()

    # login in HJ1
    def login(self):
        self.open()
        self.wait_UI(self.username_loc)
        self.__action_input_username()
        self.__action_input_password()
        self.__action_click_login()

