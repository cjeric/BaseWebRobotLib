# _*_ coding: utf-8 _*_
#!c:/Python36
#Filename: ReportPage.py

from BasePage import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
import time

class ReportPage(BasePage):
    url = ''
    # TODO functions to click button on the app bar

    # # The xpath of buttons in page-actions <div>
    # __page_action_buttons_loc = (By.XPATH, '//div[@data-hj-test-id="page-actions"]/ul/li/a')
    # __buttons_in_ellipsis_loc = (By.XPATH,'//div[@data-hj-test-id="page-actions"]/ul/li[@class="dropdown open"]/ul/li/a')

    # def __click_buttons_in_ellipsis(self, button_name):
    #     '''
    #     Click the button under ellipsis dropdown by provided name
    #     :param button_name: str: the button name in the ellipsis dropdown
    #     :return: None
    #     '''
    #     buttons = self.find_elements(*self.__buttons_in_ellipsis_loc)
    #     if len(buttons):
    #         for button in buttons:
    #             if button_name == button.text:
    #                 button.click()
    #                 return
    #     raise NoSuchElementException('The button in ellispsis button is failed to be located')

    # def __click_page_action_button(self, button_name):
    #     '''
    #     Click the button in page-action <div> by the provided name
    #     :param button_name: str: button name
    #     :return: None
    #     '''
    #     buttons = self.find_elements(*self.__page_action_buttons_loc)
    #     if len(buttons):
    #         for button in buttons: #Go throug buttons not in dorpdown.
    #             if button_name == button.text:
    #                 button.click()
    #                 return
    #         button = buttons.pop() # If nothing found in loop, then get the dropdown element
    #         button.click()
    #         self.__click_buttons_in_ellipsis(button_name) #find the button in dropdown
    #         return
    #     raise NoSuchElementException('The button is failed to be located')

    # The xpath of buttons in page-actions <div>
    __context_action_buttons_loc = (By.XPATH, '//div[@data-hj-test-id="context-actions"]/ul/li/a')

    def __click_context_action_button(self, button_name):
        '''
        Click the button in context-action <div> by the provided name. It is for the row operation on report page
        :param button_name: str: button name
        :return:
        '''
        buttons = self.find_elements(*self.__context_action_buttons_loc)
        if len(buttons):
            for button in buttons:  # Go throug buttons not in dorpdown.
                if button_name == button.text:
                    button.click()
                    return
        raise NoSuchElementException('The button is failed to be located')

    def action_page_click_button(self, button_name, group='page-action'):
        '''
        Click the buttons on app bar
        :param button_name: string, the name of the button
        :param group: string: the group the button belongs to. The option is page-action and context-action
        :return:
        '''
        # if group is None:
        #     super(ReportPage,self).action_page_click_button(button_name)
        if group == 'page-action':
            super(ReportPage,self).action_page_click_button(button_name)
            # self.__click_page_action_button(button_name)
        elif group == 'context-action':
            self.__click_context_action_button(button_name)
        else:
            raise Exception('The group must be page-action or context-action')

    # TODO functions to get and operate elements in table or row detail table

    #The container of header locator
    __table_header_container_loc = (By.CSS_SELECTOR, 'div.k-grid-header')
    #The header locator
    __table_headers_loc = (By.CSS_SELECTOR, 'th[class="k-header k-with-icon"]')

    def __get_header_elements(self):
        '''
        Return a list of header elements
        :return: a list of header elements
        '''
        page_wrap = self.get_current_page_wrap()
        headers_container = self.find_child_element(page_wrap,*self.__table_header_container_loc)
        headers = self.find_child_elements(headers_container, *self.__table_headers_loc)
        return headers

    # The xpath locator of table rows
    __table_row_loc = (By.XPATH, './/table/tbody/tr[@class="k-master-row " or @class="k-alt k-master-row " or @class="k-master-row" or @class="k-alt k-master-row" or @class="" or @class="k-alt "]')
    # The xpath locator of detail table rows related to the detail row table
    __rowdetail_row_loc = (By.XPATH, './/tbody/tr')

    def __get_table_row_elements(self, detail_name = None):
        '''
        Return the list of table rows.
        :param detail_name: string: the name of the row detail table
        :return: a list of table rows
        '''
        if detail_name is not None:
            rowdetail_table = self.__get_rowdetail_table_element(detail_name)
            table_rows = self.find_child_elements(rowdetail_table, *self.__rowdetail_row_loc)
            if len(table_rows):
                # print(len(table_rows))
                return table_rows
            else:
                raise NoSuchElementException('rows in row detail table are not located')
        else:
            page_wrap = self.get_current_page_wrap()
            table_rows = self.find_child_elements(page_wrap,*self.__table_row_loc)
            if len(table_rows):
                #print (len(table_rows))
                return table_rows
            raise NoSuchElementException('<tr> rows in table are not located')

    # The xpath locator of table cells related to table row element, but get rid of the row-indicator-cell which occurs when inline editing enabled
    __table_cell_loc = (By.XPATH,'./td[not(@style) and @class!="row-indicator-cell "]')
    # The xpath locator of cells in row detail table related to the row in row detail table
    __rowdetail_cell_loc = (By.XPATH, './td')

    def __get_table_cell_elements(self, detail_name = None):
        '''
        Return a list of table cells. The list is composed of Table[Row][column]. For Example, get 2nd cell in 1st row, then
        it should be table[0][1]
        :param detail_name: string, the name of the row detail table
        :return: a list of tabel cells, include + cell
        '''
        table = []
        if detail_name is not None:
            table_rows = self.__get_table_row_elements(detail_name)
            for row in table_rows:
                cells = self.find_child_elements(row, *self.__rowdetail_cell_loc)
                if len(cells):
                    cells.pop()  # Drop the last cell element in the list, as the last cell is an empty cell without value.
                    #print(len(cells))
                    table.append(cells)  # Add a list of cell elements in one row to the table list.
                else:
                    raise NoSuchElementException('<td> cells in row detial table not located')
            return table
        else:
            tabel_rows = self.__get_table_row_elements()
            for row in tabel_rows:
                cells = self.find_child_elements(row, *self.__table_cell_loc) #get cell elements of each row
                if len(cells):
                    cells.pop() #Drop the last cell element in the list, as the last cell is an empty cell without value.
                    table.append(cells) # Add a list of cell elements in one row to the table list.
                else:
                    raise NoSuchElementException('<td> cells in table not located')
            return table


    # TODO functions to operate table

    def get_headers(self, detail_name=None):
        '''
        Return a list of all displayed headers' name, not inculde row number
        :param detail_name: string: the name of the row detail table
        :return: a list of headers' name
        '''
        if detail_name is not None:
            rowdetail = self.__get_rowdetail_table_element(detail_name)
            headers = self.find_child_elements(rowdetail, *self.__table_headers_loc)
        else:
            headers = self.__get_header_elements()
        if len(headers):
            header_values=[]
            for header in headers:
                if header.get_attribute("style") == "display: none;":
                    continue
                header_values.append(header.get_attribute('data-title'))
            return header_values
        raise NoSuchElementException('<th> headers are not located')

    def get_values_by_row(self, row, detail_name=None):
        '''
        Get all cell values of one row in the table. The row_number starts with 1. It is actual number in the table,
        :param row: Int: The number of row in the table
        :param detail_name: string:　the name of the row detail table
        :return: a list of values in a specific row, include row number cell
        '''
        table = self.__get_table_cell_elements(detail_name)
        if not isinstance(row, int):
            raise ValueError ('row must be int')
        elif row>len(table):
            raise IndexError ('The row is out of the number of rows')
        cell_values = []
        for cell in table[row-1]:
            if cell.get_attribute('style') == 'display: none;':
                continue
            if cell.get_attribute('class') == "": # Getting rid of + cell, only add the business values to the list
                cell_values.append(cell.text)
        return cell_values

    # The xpath locator of link in table related to a cell element
    __fieldlink_loc = (By.XPATH, './/span | .//a')

    def action_cell_click(self, row, column, detail_name=None):
        '''
        Click the cell in the table. The row and column is the actual row number and column number in the table. This
        function can be used to click field link, row number, extend row details and click a label cell to highlight a
        row
        :param row: Int: The row number of the link
        :param column: Int: The column number of the link
        :param detail_name: string: the name of the row detail table
        :return: None.
        '''
        table = self.__get_table_cell_elements(detail_name)
        if not (isinstance(row,int) and isinstance(column,int)):
            raise ValueError('row or column must be int')
        elif row>len(table):
            raise IndexError('The row is out of the number of rows')
        elif column > len(table[row-1]):
            raise IndexError('The column is out of the number of columns')
        self.find_child_element(table[row-1][column-1], *self.__fieldlink_loc).click()

    # TODO functions to operate row details

    #The xpath locator of table row details
    __table_row_detail_loc = (By.XPATH,'.//hj-panelbar[@class="row-details"]/ul/li')
    #The xpath locator of row detail titles
    __table_row_detail_title_loc = (By.XPATH, './/span[@class="hj-panel-title"]')
    #The xpath locator of row detail icon
    __table_row_detail_icon_loc = (By.XPATH,'.//span[@class="k-icon k-i-arrow-s k-panelbar-expand"]')

    def __get_rowdetail_table_element(self, detail_name):
        '''
        Return the row detail table by provided table name
        :param detail_name: string, the row detail table name
        :return: a row detail table element
        '''
        titles = self.get_rowdetail_titles()
        page_wrap = self.get_current_page_wrap()
        table_row_details = self.find_child_elements(page_wrap, *self.__table_row_detail_loc)
        index = 0
        for title in titles:
            if title == detail_name:
                return table_row_details[index]
            else:
                index += 1
        raise NoSuchElementException('detail row table does not exist')

    def get_rowdetail_titles(self):
        '''
        Get the titles of all row detail tables
        :return: a list of table titles
        '''
        page_wrap = self.get_current_page_wrap()
        WebDriverWait(self.driver, self.timeout, 0.5).until(EC.visibility_of_element_located((By.XPATH,'//span[@class="hj-panel-title"]')))
        row_detail_titles = self.find_child_elements(page_wrap, *self.__table_row_detail_title_loc)
        if len(row_detail_titles):
            titles=[]
            for titel in row_detail_titles:
                titles.append(titel.text)
            return titles
        raise NoSuchElementException('detail row titles are not located')

    def action_extend_rowdetail(self, detail_name):
        '''
        Extend the row detail table by provided table name
        :param detail_name: string, the name of the row detail table
        :return: None
        '''
        titles = self.get_rowdetail_titles()
        page_wrap = self.get_current_page_wrap()
        row_detail_icons = self.find_child_elements(page_wrap, *self.__table_row_detail_icon_loc)
        index = 0
        for title in titles:
            if title == detail_name:
                row_detail_icons[index].click()
                return
            else:
                index+=1
        raise NoSuchElementException('detail row icon does not exist')




