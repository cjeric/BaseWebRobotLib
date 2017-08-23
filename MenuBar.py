# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: MenuBar.py

from Base import Base
from selenium.webdriver.common.by import By
import time


class MenuBar(Base):
    url = ''

    #Menu button locator
    menu_button_loc = (By.ID,'menuButtonToggle')

    def action_toggle_menu(self):
        '''
        Make the menu tree display
        :return: None
        '''
        self.find_element(*self.menu_button_loc).click()

    #Menu locators for different status
    menu_current_loc = (By.XPATH, '//nav[@id="menu"]/ul/li[@class="home current"]/a')
    menu_ancestor_loc = (By.XPATH, '//nav[@id="menu"]/ul/li[@class="home ancestor"]/a')

    def action_backto_menu(self):
        '''
        Click the Menu in the menu tree to back to the root level
        :return: None
        '''
        self.find_element(*self.menu_ancestor_loc).click()

    #Entry menu locator
    app_group_loc = (By.XPATH,'//nav[@id="menu"]/ul/li[@class="with-children closed"]/a')

    #Extend app group
    def action_expand_app_group(self, groupName):
        '''
        Expand the application group
        :param groupName: The application group want to extend
        :return: None
        '''
        group_list = self.find_elements(*self.app_group_loc)
        for group in group_list:
            if group.text == groupName:
                group.click()
                break
    # The locator of the opened menu
    __current_open_menu_loc = (By.XPATH, '//li[@class="with-children current open"] | //li[@class="with-children open current"]')
    # The locator of the sub menu to extend
    __menu_toextend_loc = (By.XPATH, './/li[@class="with-children closed"]/a')
    # The locator of the page to open
    __page_toopen_loc = (By.XPATH, './/li[@class="without-children closed"]/a')

    # Click the submenu or page under the current opened menu
    def action_expand_menu(self, menu, isMenu = True):
        '''
        Expand the sub menu or open the page
        :param menu: The name of menu item
        :param isMenu: whether the link is a submenu
        :return:
        '''
        open_menu = self.wait_UI(self.__current_open_menu_loc)
        if isMenu:
            menu_items_loc = self.__menu_toextend_loc
        else:
            menu_items_loc = self.__page_toopen_loc
        menu_items = open_menu.find_elements(*menu_items_loc)
        for menu_item in menu_items:
            if menu_item.text == menu:
                menu_item.click()
                break

    #The locator of the current opened menu's parent menus
    __ancestor_menu_loctor = (By.XPATH, '//li[@class="with-children open ancestor"]/a')

    #Click the parent menu of the current opened one
    def action_collapse_menu(self, menu):
        '''
        Collapse a specific menu, except the root Menu
        :param menuName: The menu want to be collapsed
        :return:
        '''
        menu_items = self.find_elements(*self.__ancestor_menu_loctor)
        for menu_item in menu_items:
            if menu_item.text == menu:
                menu_item.click()
                break


