# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: SearchPage.py

from BasePage import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
from selenium.webdriver.support import select
from robot.api import logger
import time


class SearchPage(BasePage):
    url = ''
    # TODO Functions to find the specific  hj-field-group-row. hj-field-group-row contains label and the UI.hj-field-group-row is used as parent element to help locate the deeper UI controls

    # The locator of the all field groups
    __field_groups_loc = (By.CSS_SELECTOR, 'div[data-hj-test-id="field-table"]>hj-field-table-row')
    __field_group_name_loc = (By.ID, 'field-group_title')

    def __get_field_cells_path(self, groupIndex):
        '''
        Return hj-feild-cell css selector path according to the group index input. Index starts from 1   
        :param groupIndex: The field group user want
        :return: the css selector of all field group rows
        '''
        logger.debug('Start to get css selector of all fields under groupIndex %d' % groupIndex)
        field_groups_list_length = len(self.find_elements(*self.__field_groups_loc))
        if not isinstance(groupIndex, int):
            raise ValueError ('groupIndex must be int')
        elif groupIndex>field_groups_list_length:
            print(field_groups_list_length)
            raise IndexError ('The groupIndex is out of the number of groups')
        field_group_rows_path = 'div[data-hj-test-id="field-table"]>hj-field-table-row:nth-of-type(' + str(groupIndex) \
                                + ')>div[data-hj-test-id="field-table-row"]>hj-field-group>div[data-hj-test-id="field-group"]>div[data-hj-test-id="field-group-content"]>hj-field-group-row'
        field_cells_path = field_group_rows_path+'>div>hj-field-cell'
        return field_cells_path

    # The  CSS locator of the hj-field-label related to hj-field-group-row element
    __field_label_loc = (By.CSS_SELECTOR, 'hj-field-label[data-hj-test-id="field-label"]')
    # The CSS locator of the hj-field-control name related to hj-field-group-row element
    __field_control_loc = (By.CSS_SELECTOR, 'hj-field-control[data-hj-test-id="field-control"]')

    def __get_field_control(self, name, groupIndex):
        '''
        Return the hj-field-control by control's label name
        :param groupIndex: The field group the control located in
        :param name: The control's label name
        :return: Return the hj-field-control web element
        '''
        logger.debug('Start to get hj-field-control (UI controller wraper of field %s)' % name)
        page_wrap = self.get_current_page_wrap() # Get the current displayed page wrap
        field_cell_loc =(By.CSS_SELECTOR, self.__get_field_cells_path(groupIndex))
        field_cells = self.find_child_elements(page_wrap,*field_cell_loc) #Get all hj-field-cell elements in the hj-field-table-row only in displayed page
        counter = 1
        if len(field_cells): # Go throuth each hj-field-cell, return hj-field-control if the text matches name input
            for cell in field_cells:
                text = self.find_child_element(cell, *self.__field_label_loc).text
                if text == name:
                    field_control = self.find_child_element(cell, *self.__field_control_loc)
                    return field_control
                else:
                    counter+=1
        raise NoSuchElementException('hj-field-group-row not found by the provided name and groupIndex')

    # TODO Functions for the dropdown list operations. The functions are independent, not based on any other UI controls.

    # The locator of all div<k-list-container>. k-list-container is the container of the dropdown list in the page
    __list_container_loc = (By.CLASS_NAME, 'k-list-container')
    # The locator of the dropdown list items. It is related to the div<k-list-container> element.
    __list_container_items_loc = (By.TAG_NAME, 'li')

    def __get_list_container(self):
        '''
        Find all div<k-list-container>, but only return the one is displayed.
        :return: div<k-list-container>
        '''
        logger.debug('Get current displayed list container (Find the current used dropdown list)')
        list_containers= self.find_elements(*self.__list_container_loc)
        for list_container in list_containers:
            if list_container.is_displayed():
                return list_container

    def __get_list_container_items(self):
        '''
        Get all options/items under dropdown list (div<k-list-container>). Before use the function, have to expand
        dropdown list first
        :return: the items list
        '''
        logger.debug('Get all items under the current displayed drop down list')
        list_container = self.__get_list_container()
        dropdown_list_items = self.find_child_elements(list_container, *self.__list_container_items_loc)
        if len(dropdown_list_items):
            items_text_list = []
            for dropdown_list_item in dropdown_list_items:
                items_text_list.append(dropdown_list_item.text)
            return items_text_list
        raise NoSuchElementException('The item in dropdown list is not located')

    def __select_from_dropdown(self, text):
        '''
        Select specific text in dropdown list which provied by user
        :param text: The item in dropdown list want to be selected
        :return: None
        '''
        logger.debug('select %s in drop down list' % text)
        list_container = self.__get_list_container()
        dropdown_list_items = self.find_child_elements(list_container, *self.__list_container_items_loc)
        if len(dropdown_list_items):
            for dropdown_list_item in dropdown_list_items:
                if dropdown_list_item.text == text:
                    dropdown_list_item.click()
                    return
        raise NoSuchElementException('The item in dropdown list is not located')

    # TODO General fucntions to operate the search page not based on any specific UI controls.

    def get_all_labels_name(self, groups_number=1):
        '''
        Return all label names on the page
        :param groups_number: The number of field groups, default value is 1
        :return: a list contains all label names in the page
        '''
        logger.info('Get all fields names on page')
        if not isinstance(groups_number, int):
            raise ValueError('groups_numbers must be int')
        name_list = []
        for i in range(1, groups_number+1):
            page_wrap = self.get_current_page_wrap() #Get the current displayed page_wrap
            field_cell_loc = (By.CSS_SELECTOR, self.__get_field_cells_path(i))
            field_cells = self.find_child_elements(page_wrap, *field_cell_loc)  # Get all hj-field-cell elements only in the displayed page wrap
            if len(field_cells):  # Go throuth each row, return hj-field-control if the text matches name input
                for cell in field_cells:
                    text = self.find_child_element(cell, *self.__field_label_loc).text
                    name_list.append(text)
            else:
                raise NoSuchElementException('Field group rows are not located')
        return name_list

    # TODO fucntions to locate and operate the checkbox control.

    # The CSS locator of the hj-checkbox related to hj-field-control element
    __checkbox_loc = (By.CSS_SELECTOR, 'hj-checkbox>div>input.k-checkbox')

    def __get_checkbox_element(self, name, groupIndex):
        '''
        Return the hj-checkbox web element
        :param groupIndex: The field group the control located in
        :param name: The control's label name
        :return: hj-checkbox element
        '''
        logger.debug('Get checkbox element by field name')
        field_control = self.__get_field_control(name, groupIndex)
        checkbox_element = self.find_child_element(field_control, *self.__checkbox_loc)
        if checkbox_element.get_attribute("type") == "checkbox":
            return checkbox_element
        else:
            raise NoSuchAttributeException('It is not a checkbox')

    def action_checkbox_check(self, name, groupIndex=1):
        '''
        Check/uncheck the checkbox
        :param groupIndex: The field group the control located in, default is 1
        :param name: The control's label name
        :return: None
        '''
        logger.info(r'Check/uncheck checkbox %s' % name)
        checkbox_element = self.__get_checkbox_element(name, groupIndex)
        checkbox_element.click()

    # TODO fucntions to locate and operate the textbox related controls. Support edit and masked edit controls

    # The CSS locator of the hj-textbox and hj-password-text related to hj-field-control element
    __edit_loc = (By.CSS_SELECTOR, 'input.k-textbox')

    def __get_edit_element(self, name, groupIndex):
        '''
        Return the hj-textbox and hj-password-textbox web element
        :param groupIndex: The field group the control located in
        :param name: The control's label name
        :return: hj-textbox or hj-passowrd-textbox element
        '''
        logger.debug('Get textbox element by field name')
        field_control = self.__get_field_control(name, groupIndex)
        edit_element = self.find_child_element(field_control, *self.__edit_loc)
        return edit_element

    def action_edit_input(self,name, value, groupIndex=1):
        '''
        Input values to edit and masked edit control
        :param groupIndex: The field group the control located in, default is 1
        :param name: The control's label name
        :param value: The value input
        :return: None
        '''
        logger.info('Input %s to textbox %s' % (value, name))
        edit_element = self.__get_edit_element(name, groupIndex)
        edit_element.send_keys(value)

    def action_edit_clear(self,name,groupIndex=1):
        '''
        Clear the value in edit and masked edit control
        :param name: string, The control's label name
        :param groupIndex: Integer: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Clear value in textbox %s' % name)
        edit_element = self.__get_edit_element(name, groupIndex)
        edit_element.clear()

    # TODO fucntions to locate and operate the multi edit control.

    # The CSS locator of the hj-multiline-textbox related to hj-field-control element
    __multiedit_loc = (By.CSS_SELECTOR, 'hj-multiline-textbox>textarea.k-textbox')

    def __get_multiedit_element(self, name, groupIndex):
        '''
        Return the hj-multieline-textbox web element
        :param groupIndex: The field group the control located in
        :param name: The control's label name
        :return: hj-multieline-textbox element
        '''
        logger.debug('Get multi textbox element')
        field_control = self.__get_field_control(name, groupIndex)
        multiedit_element = self.find_child_element(field_control, *self.__multiedit_loc)
        return multiedit_element

    def action_multiedit_input(self,name, value,groupIndex=1 ):
        '''
        Input values to multiedit control
        :param groupIndex: The field group the control located in, default is 1
        :param name: The control's label name
        :param value: The value input
        :return: None
        '''
        logger.info('Input %s to multi textbox %s' % (value, name))
        multiedit_element = self.__get_multiedit_element(name, groupIndex)
        multiedit_element.send_keys(value)

    def action_multiedit_clear(self,name,groupIndex=1):
        '''
        Clear the value in multiedit control
        :param name: string, The control's label name
        :param groupIndex: Integer: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Clear value in multi textbox %s' % name)
        multiedit_element = self.__get_multiedit_element(name, groupIndex)
        multiedit_element.clear()

    # TODO fucntions to locate and operate the search like control.

    # The CSS locator of the searchlike control related to hj-field-control element
    __searchlike_textbox_loc = (By.CSS_SELECTOR, 'div.searchLike-control-textbox-container>hj-textbox>input')
    __searchlike_button_loc = (By.CSS_SELECTOR, 'div.searchLike-control-dropdownlist-container>hj-dropdownlist>span>span>span.k-select')
    __searchlike_locs = [__searchlike_button_loc, __searchlike_textbox_loc]

    def __get_searchlike_element(self, name, groupIndex):
        '''
        Get the searchlike components. The return is a list. list[0] is the dropdown list button. list[1]
        is the textbox for search text input.
        :param groupIndex: The field group the control located in
        :param name: The control's label name
        :return: The searchlike control components list
        '''
        logger.debug('Get UI components in searchlike controller')
        searchlike_elements=[]
        for loc in self.__searchlike_locs:
            field_control = self.__get_field_control(name, groupIndex)
            searchlike_element = self.find_child_element(field_control, *loc)
            searchlike_elements.append(searchlike_element)
        return searchlike_elements

    def action_searchlike_input(self, name, value, groupIndex=1, search_type="Like"):
        '''
        Select the search type and then input the search value. list[0] is the dropdown list button. list[1]
        is the textbox for search text input
        :param name: The control's label name
        :param value: The search value
        :param groupIndex: The field group the control located in, default is 1
        :param search_type: The search type in the dropdown list, default is like. The acceptable value, is Like, Exactly
        :return: None
        '''
        logger.info('Search %s %s via searchlike %s' %(search_type, value, name))
        searchlike_elements = self.__get_searchlike_element(name, groupIndex)
        searchlike_elements[0].click()
        time.sleep(1)
        self.__select_from_dropdown(search_type)
        searchlike_elements[1].send_keys(value)

    def action_searchlike_clear(self,name,groupIndex=1):
        '''
        Clear the value in searchlike control
        :param name: string, The control's label name
        :param groupIndex: Integer: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Clear textbox in searchlike %s' % name)
        searchlike_elements = self.__get_searchlike_element(name, groupIndex)
        searchlike_elements[1].clear()

    # TODO fucntions to locate and operate the dorpdown list related controls. Support drop down list and Time controls

    # The CSS locator of the dropdown list button control related to hj-field-control element
    __dropdown_button_loc = (By.CSS_SELECTOR, 'span.k-select')

    def __get_dropdown_button_element(self, name, groupIndex):
        '''
        Get the button element of the drop down list
        :param name: The control's label name
        :param groupIndex: The field group the control located in
        :return: drop down button element
        '''
        logger.debug('Get button element in dropdown list')
        field_control = self.__get_field_control(name, groupIndex)
        dropdown_button = self.find_child_element(field_control, *self.__dropdown_button_loc)
       # dropdown_button = field_control.find_element_by_css_selector(self.__dropdown_button_loc)
        return dropdown_button

    def get_dropdown_options(self, name, groupIndex=1):
        '''
        Return a list of all options in the dropdown list
        :param name: The control's label name
        :param groupIndex: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Get items in drop down list %s' % name)
        self.__get_dropdown_button_element(name, groupIndex).click()
        dropdown_options =  self.__get_list_container_items()
        self.__get_dropdown_button_element(name, groupIndex).click()
        return dropdown_options

    def action_dropdown_select(self, name, value, groupIndex=1):
        '''
        Select the specific option in the dropdown list by the value provided
        :param name: The control's label name
        :param value: The option's text you want to select
        :param groupIndex: The field group the control located in, default is 1
        :return: None
        '''
        logger.info('Select %s in drop down list %s' %(value, name))
        dropdown_button = self.__get_dropdown_button_element(name, groupIndex)
        dropdown_button.location_once_scrolled_into_view
        time.sleep(1)
        dropdown_button.click()
        self.__select_from_dropdown(value)

    # TODO fucntions to input value to the textbox of dropdown list, such as Calendar, Calendar&Time, Time, Dropdown

    # The CSS locator of the calendar and calendar&time control related to hj-field-control element
    __dropdown_textbox_loc = (By.CSS_SELECTOR, 'input.k-input')

    def __get_dropdown_textbox_element(self, name, groupIndex):
        '''
        Return the textbox of the calendar and calendar&time controls
        :param name: The control's label name
        :param groupIndex: The field group the control located in
        :return: calendar or calendar&time textbox element
        '''
        logger.debug('Get textbox in drop down list')
        field_control = self.__get_field_control(name, groupIndex)
        calendar_textbox = self.find_child_element(field_control, *self.__dropdown_textbox_loc)
        return calendar_textbox

    def action_dropdown_input(self, name, value, groupIndex=1):
        '''
        Input value to the textbox of calendar, time and calendar&time controls
        :param name: The control's label name
        :param value: The option's text you want to input
        :param groupIndex: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Input %s to drop down list %s' % name)
        calendar_textbox = self.__get_dropdown_textbox_element(name, groupIndex)
        calendar_textbox.clear()
        calendar_textbox.send_keys(value)

    def _get_value(self):
        '''
        Not finished
        :return: string 
        '''
        element = self.__get_edit_element('Edit', 2)
        print(element.get_attribute('value'))

    # TODO fucntions to locate and operate the listbox control.

    # The CSS locator of the listbox control related to hj-field-control element
    __listbox_loc = (By.CSS_SELECTOR, 'hj-listbox>select')

    def __get_listbox_element(self, name, groupIndex):
        '''
        Get the listbox element.
        :param name: String. The control's label name
        :param groupIndex: Int. The field group the control located in.
        :return: Return listbox element
        '''
        logger.debug('Get listbox web element')
        field_control = self.__get_field_control(name, groupIndex)
        listbox_control = self.find_child_element(field_control, *self.__listbox_loc)
        return listbox_control

    def action_listbox_select(self, name, value, groupIndex=1):
        '''
        Select a value in listbox.
        :param name: The control's label name
        :param value: The option's text you want to select
        :param groupIndex: The field group the control located in, default is 1
        :return:
        '''
        logger.info('Select %s in listbox %s' %(value, name))
        listbox = select.Select(self.__get_listbox_element(name, groupIndex))
        listbox.select_by_visible_text(value)

    # TODO function to locate and operate the label control

    #the css selector for hj-label
    __label_loc = (By.CSS_SELECTOR, 'hj-label>span')

    def __get_label_element(self, name, groupIndex):
        '''
        Get the label element
        :param name: String. The control's label name
        :param groupIndex: Int. The field group the control located in.
        :return: label element
        '''
        logger.debug('Get label web element')
        field_control = self.__get_field_control(name, groupIndex)
        label_control = self.find_child_element(field_control, *self.__label_loc)
        return label_control

    #TODO functions to get error message

    #The xpath locator for page error hint
    __page_error_loc = (By.XPATH, '//div[@class="hj-page-validation-errors-message"]')

    def get_page_error(self):
        '''
        Get the page error hint value
        :return: string, error message
        '''
        logger.info('Get error message displayed under page title')
        return self.wait_UI(self.__page_error_loc).text

    __field_error_loc = (By.XPATH, '//span[@data-hj-test-id="field-error"]')

    def get_field_errors(self):
        '''
        Return a list of all fields error messages
        :return: a list of text
        '''
        logger.info('Get error messages displayed on fields')
        self.wait_UI(self.__field_error_loc)
        field_errors = self.find_elements(*self.__field_error_loc)
        error_messages=[]
        for error in field_errors:
            error_messages.append(error.text)
        return error_messages




