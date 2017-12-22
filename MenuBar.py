# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: MenuBar.py

from BasePage import BasePage
from selenium.webdriver.common.by import By
from robot.api import logger
from selenium.common.exceptions import NoSuchElementException
import time

class MenuBar(BasePage):
    url = ''


    #Menu button locator
    menu_button_loc = (By.ID, 'menuButtonToggle')

    def action_toggle_menu(self):
        '''
        Make the menu tree display
        :return: None
        '''
        logger.info('Toggle menu')
        self.find_element(*self.menu_button_loc).click()

    #Menu locators for different status
    menu_current_loc = (By.XPATH, '//nav[@id="menu"]/ul/li[@class="home current"]/a')
    menu_ancestor_loc = (By.XPATH, '//nav[@id="menu"]/ul/li[@class="home ancestor"]/a')

    def action_backto_menu(self):
        '''
        Click the Menu in the menu tree to back to the root level
        :return: None
        '''
        logger.info('Back to root of menu tree')
        self.find_element(*self.menu_ancestor_loc).click()

    #Entry menu locator
    app_group_loc = (By.XPATH, '//nav[@id="menu"]/ul/li[@class="with-children closed"]/a')

    #Extend app group
    def action_expand_app_group(self, groupName):
        '''
        Expand the application group
        :param groupName: The application group want to extend
        :return: None
        '''
        logger.info('Extend application %s' % groupName)
        group_list = self.find_elements(*self.app_group_loc)
        if len(group_list)>0:
            for group in group_list:
                if group.text == groupName:
                    logger.debug('Application %s is found' % group.text)
                    group.click()
                    return
        raise NoSuchElementException ('Fail to expand app group. The application %s not found' % groupName)

    # The locator of the opened menu
    __current_open_menu_loc = (By.XPATH, '//li[@class="with-children current open"] | //li[@class="with-children open current"]')
    # The locator of the sub menu to extend
    __menu_toextend_loc = (By.XPATH, './/li[@class="with-children closed"]/a')
    # The locator of the page to open
    __page_toopen_loc = (By.XPATH, './/li[@class="without-children closed"]/a')

    # Click the submenu or page under the current opened menu
    def action_expand_menu(self, menu, isMenu = True, title = None):
        '''
        Expand the sub menu or open the page
        :param menu: The name of menu item
        :param isMenu: whether the link is a submenu
        :return: None
        '''
        logger.info('Extend submenu or open page %s' % menu)
        open_menu = self.wait_UI(self.__current_open_menu_loc)
        if isMenu:
            menu_items_loc = self.__menu_toextend_loc
        else:
            menu_items_loc = self.__page_toopen_loc
        menu_items = open_menu.find_elements(*menu_items_loc)
        if len(menu_items)>0:
            for menu_item in menu_items:
                if menu_item.text == menu:
                    logger.debug('Application %s is found and click it' % menu_item.text)
                    menu_item.click()
                    if not isMenu and title is not None:
                        logger.debug('Wait page to load')
                        self.wait_page(title)
                    return
        raise NoSuchElementException('Fail to expand Menu or open page, %s not found' % menu)

    def navi_to_page(self, group, page_title, *submenu_list):
        '''
        Navi to the page according to the provided menu path
        :param group: app group name
        :param page_title: page title
        :param submenu_list: the list of menu path
        :return: 
        '''
        self.action_toggle_menu()
        time.sleep(1)
        self.action_expand_app_group(group)
        counter = 0
        for item in submenu_list:
            if counter == len(submenu_list) - 1:
                self.action_expand_menu(submenu_list[counter], False, page_title)
            else:
                self.action_expand_menu(submenu_list[counter])
                counter += 1

    #The locator of the current opened menu's parent menus
    __ancestor_menu_loctor = (By.XPATH, '//li[@class="with-children open ancestor"]/a')

    #Click the parent menu of the current opened one
    def action_collapse_menu(self, menu):
        '''
        Collapse a specific menu, except the root Menu
        :param menuName: The menu want to be collapsed
        :return: None
        '''
        logger.info('collapse menu %s' % menu)
        menu_items = self.find_elements(*self.__ancestor_menu_loctor)
        if len(menu_items)>0:
            for menu_item in menu_items:
                if menu_item.text == menu:
                    logger.debug('menu item %s is found' % menu_item.text)
                    menu_item.click()
                    return
        raise NoSuchElementException ('Fail to collapse menu. %s not found' % menu)


