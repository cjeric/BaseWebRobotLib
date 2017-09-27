# _*_ coding: utf-8 _*_
# !c:/Python36
# Filename: BasePage.py

from Base import Base as _Base
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger
import time

class BasePage(_Base):
    url = ''

    #TODO functions to operate page

    #The css selector of the current displayed page wrap
    __page_wrap_loc = (
    By.CSS_SELECTOR, 'div[class="hj-spaces-page-wrap supply-chain-advantage"][style="outline: medium none;"]')

    def get_current_page_wrap(self):
        '''
        Get the current displayed page wrap element
        :return: page wrap web element
        '''
        logger.info('Get current displayed page')
        return self.wait_UI(self.__page_wrap_loc)

    # page header locator
    __page_header_loc = (By.CSS_SELECTOR, 'div[data-hj-test-id="hj-active-thread-title"]')
    # Return the page header
    def get_header(self):
        logger.info('Get page header')
        return self.find_element(*self.__page_header_loc).text

    #title locator
    __page_title_loc = (By.CSS_SELECTOR, 'span[data-hj-test-id="hj-active-page-title"]')

    def get_page_title(self):
        '''
        Return the page title by title_locator
        :return: The text of the page title
        '''
        logger.info('Get page title')
        title = self.wait_UI(self.__page_title_loc)
        logger.debug('page title is %s' % title.text)
        return title.text

    # __footertext_loc = (By.CSS_SELECTOR, 'span.footer-text')

    def wait_page(self, page_title):
        '''
        Wait the specific page loaded.
        :param page_type: The type of page you want to wait
        :return: None
        '''
        logger.info('wait page %s to display' % page_title)
        for i in range(self.timeout):
            title = self.get_page_title()
            if page_title == title:
                logger.debug('Page %s displays' % page_title)
                return True
            else:
                time.sleep(1)
        logger.debug('Actual page title is %s, expected page is %s' % (title, page_title))
        raise TimeoutException('Fail to open page %s' % page_title)

    __previous_button_loc = (By.XPATH, '//a[@data-hj-test-id="active-thread-previous-button"]')
    __next_button_loc = (By.XPATH, '//a[@data-hj-test-id="active-thread-next-button"]')

    def action_page_next(self):
        logger.info('Forward to next page')
        if EC.element_to_be_clickable(self.__next_button_loc):
            self.find_element(*self.__next_button_loc).click()
        else:
            raise Exception('The next button is not clickable')

    def action_page_previous(self):
        logger.info('Back to previous page')
        if EC.element_to_be_clickable(self.__previous_button_loc):
            self.find_element(*self.__previous_button_loc).click()
        else:
            raise Exception('The previous button is not clickable')

    # TODO functions to click buttons

    # The xpath of buttons in page-actions <div>
    __page_action_buttons_loc = (By.XPATH, '//div[@data-hj-test-id="page-actions"]/ul/li/a')
    __buttons_in_ellipsis_loc = (By.XPATH, '//div[@data-hj-test-id="page-actions"]/ul/li[@class="dropdown open"]/ul/li/a')

    def __click_buttons_in_ellipsis(self, button_name):
        '''
        Click the button under ellipsis dropdown by provided name
        :param button_name: str: the button name in the ellipsis dropdown
        :return: None
        '''
        logger.debug('Click the button %s in ellipsis drop down list' % button_name)
        buttons = self.find_elements(*self.__buttons_in_ellipsis_loc)
        if len(buttons):
            for button in buttons:
                if button_name == button.text:
                    button.click()
                    return
        raise NoSuchElementException('The button in ellispsis button is failed to be located')

    def action_page_click_button(self, button_name):
        '''
        Click the button in page-action <div> by the provided name
        :param button_name: str: button name
        :return: None
        '''
        logger.info('Click button %s' % button_name)
        buttons = self.find_elements(*self.__page_action_buttons_loc)
        if len(buttons):
            for button in buttons: #Go throug buttons not in dorpdown.
                if button_name == button.text:
                    button.click()
                    return
            button = buttons.pop() # If nothing found in loop, then get the dropdown element
            button.click()
            self.__click_buttons_in_ellipsis(button_name) #find the button in dropdown
            return
        raise NoSuchElementException('The button is failed to be located')

    # TODO functions to operate information dialog

    #The xpath locator of the information dialog
    __info_dialog_loc = (By.XPATH, '//hj-information-dialog[@data-hj-test-id="hj-workspace-page-information-dialog"]')
    #The xpath locator of the information dialog title related to information dialog element
    __info_dialog_title_loc = (By.XPATH, './/span[@data-hj-test-id="information-dialog-title"]')
    # The xpath locator of the information dialog header related to information dialog element
    __info_dialog_header_loc = (By.XPATH, './/span[@data-hj-test-id="information-dialog-header"]')
    # The xpath locator of the information dialog message related to information dialog element
    __info_dialog_message_loc = (By.XPATH, './/div[@data-hj-test-id="information-dialog-message"]')
    # The xpath locator of the all type of dialog buttons related to dialog element
    __dialog_buttons_loc = (By.XPATH, './/button[@class="k-button"]')

    def __get_information_dialog(self):
        '''
        Get information dailog element
        :return: information dialog web element
        '''
        logger.debug('Get information dialog web element')
        return self.wait_UI(self.__info_dialog_loc)

    def __get_information_buttons(self):
        '''
        Get buttons of the information dialog
        :return: a list of button elements
        '''
        logger.debug('Get buttons web elements on information dialog')
        info_dialog = self.__get_information_dialog()
        return self.find_child_elements(info_dialog, *self.__dialog_buttons_loc)

    def get_infodialog_title(self):
        '''
        Return the info dialog title text
        :return: string: the info dialog title text
        '''
        logger.info('Get infomation dialog title')
        info_dialog = self.__get_information_dialog()
        return self.find_child_element(info_dialog, *self.__info_dialog_title_loc).text

    def get_infodialog_header(self):
        '''
        Return the info dialog header text
        :return: string: the info dialog header text
        '''
        logger.info('Get infomation dialog header')
        info_dialog = self.__get_information_dialog()
        return self.find_child_element(info_dialog, *self.__info_dialog_header_loc).text

    def get_infodialog_message(self):
        '''
        Return the info dialog message text
        :return: string: the info dialog message text
        '''
        logger.info('Get infomation dialog message')
        info_dialog = self.__get_information_dialog()
        return self.find_child_element(info_dialog, *self.__info_dialog_message_loc).text

    def action_infodialog_click_button(self, button_name):
        '''
        Click the button by provided name
        :param button_name: string, the name of the button
        :return: None
        '''
        logger.info('Click % button on information dailog' % button_name)
        buttons = self.__get_information_buttons()
        if len(buttons):
            for button in buttons:
                if button.text == button_name:
                    button.click()
                    return
        raise NoSuchElementException('No buttons found or the button_name is not correct')

    # TODO functions to operate error dialog

    #The xpath locator of the information dialog
    __error_dialog_loc = (By.XPATH, '//hj-error-dialog[@data-hj-test-id="hj-workspace-page-error-dialog"]')
    # The xpath locator of the information dialog message related to information dialog element
    __error_dialog_message_loc = (By.XPATH, './/div[@class="hj-dlg-content"]')

    def __get_error_dialog(self):
        '''
        Get error dailog element
        :return: error dialog web element
        '''
        logger.debug('Get error dialog web element')
        return self.wait_UI(self.__error_dialog_loc)

    def __get_error_buttons(self):
        '''
        Get buttons of the error dialog
        :return: a list of button elements
        '''
        logger.debug('Get buttons web element on error dialog')
        info_dialog = self.__get_error_dialog()
        return self.find_child_elements(info_dialog, *self.__dialog_buttons_loc)

    def get_errordialog_message(self):
        '''
        Return the error dialog message text
        :return: string: the error dialog message text
        '''
        logger.info('Get error dialog message')
        info_dialog = self.__get_error_dialog()
        return self.find_child_element(info_dialog, *self.__error_dialog_message_loc).text

    def action_errordialog_click_button(self, button_name):
        '''
        Click the button by provided name
        :param button_name: string, the name of the button
        :return: None
        '''
        logger.info('Click %s button on error dialog' % button_name)
        buttons = self.__get_error_buttons()
        if len(buttons):
            for button in buttons:
                if button.text == button_name:
                    button.click()
                    return
        raise NoSuchElementException('No buttons found or the button_name is not correct')


