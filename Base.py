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
        '''
        Navigate to the specific url via browser
        :param url: string, url to go to
        :return: 
        '''
        logger.debug(r'start Base._open')
        url = self.base_url + url
        self.driver.get(url)
        assert self.on_page(), 'Did not access to %s' % url

    def find_element(self, *locators):
        '''
        Find web element by UI locators
        :param locators: a tuple of UI locators
        :return: a web element
        '''
        logger.debug('find element %s by %s' %(locators[1], locators[0]))
        return self.driver.find_element(*locators)

    def find_elements(self, *locators):
        '''
        Find web elements by UI locators
        :param locators: a tuple of UI locators
        :return: a list of web elements
        '''
        logger.debug('find elements %s by %s' % (locators[1], locators[0]))
        return self.driver.find_elements(*locators)

    def find_child_element(self, webelement, *locators):
        '''
        Finde web element under a parent UI by UI locators
        :param webelement: web element, the parent UI
        :param locators: a tuple of UI locators
        :return: a web element
        '''
        logger.debug('find child element %s by %s under %s' % (locators[1], locators[0], webelement))
        return webelement.find_element(*locators)

    def find_child_elements(self, webelement, *locators):
        '''
        Finde web elements under a parent UI by UI locators
        :param webelement: web element, the parent UI
        :param locators: a tuple of UI locators
        :return: a list of web elements
        '''
        logger.debug('find child elements %s by %s under %s' % (locators[1], locators[0], webelement))
        return webelement.find_elements(*locators)

    def open(self):
        '''
        Call private _open menthod
        :return: None
        '''
        logger.debug(r'open the url %s' % self.url)
        self._open(self.url)

    def on_page(self):
        '''
        Verify the browser go to the expected url
        :return: boolen
        '''
        return self.driver.current_url == (self.base_url + self.url)

    def script(self, src):
        '''
        Run the script codes given
        :param src: scripts definition
        :return: 
        '''
        logger.debug('run scripts %s' % src)
        return self.driver.execute_script(src)

    def wait_UI(self, *locators):
        '''
        Wait the UI to display on page
        :param locators: tuple of UI locators
        :return: web element
        '''
        logger.debug(r'wait UI %s by %s' %(locators[0][1], locators[0][0]))
        return WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located(*locators))

    def quit_browser(self):
        '''
        Close the browser
        :param driver: brwoser instance
        :return: 
        '''
        logger.debug('Close the browser')
        self.driver.close()

