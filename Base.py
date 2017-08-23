# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: Base.py
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger


class Base(object):
    '''base page object'''

    home_page = 'http://sca12r2ss12c:30000/core/Default.html'

    def __init__(self, driver, base_url = home_page, parent = None):
        logger.debug('start Base initialization')
        self.driver = driver
        self.base_url = base_url
        self.timeout = 30
        self.parent = parent

    def _open(self,url):
        logger.debug(r'start Base._open')
        url = self.base_url + url
        self.driver.get(url)
        assert self.on_page(), 'Did not access to %s' % url

    def find_element(self, *locators):
        logger.debug('find element %s by %s' %)
        return self.driver.find_element(*locators)

    def find_elements(self, *locators):
        return self.driver.find_elements(*locators)

    def find_child_element(self, webelement, *locators):
        return webelement.find_element(*locators)

    def find_child_elements(self, webelement, *locators):
        return webelement.find_elements(*locators)

    def open(self):
        logger.debug(r'open the url %s' % self.url)
        self._open(self.url)

    def on_page(self):
        return self.driver.current_url == (self.base_url + self.url)

    def script(self, src):
        return self.driver.execute_script(src)

    def wait_UI(self, *locators):
        logger.debug(r'start Base.wati_UI')
        return WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located(*locators))

