*** Settings ***
Library           WebAuto.BasePage    ${browser}

*** Keywords ***
click page button
    [Arguments]    ${buttonName}
    WebAuto.BasePage.action page click button    ${buttonName}

get page title
    ${title}    WebAuto.BasePage.get page title
    [Return]    ${title}

get current page wrap
    ${page_wraper}    WebAuto.BasePage.get current page wrap
    [Return]    ${page_wraper}

wait page
    [Arguments]    ${page title}
    WebAuto.BasePage.wait page    ${page title}

next page
    WebAuto.BasePage.action page next

previous page
    WebAuto.BasePage.action page previous

click button
    [Arguments]    ${button name}
    WebAuto.BasePage.action page click button    ${button name}

get infodialog title
    ${title}    WebAuto.BasePage.get infodialog title
    [Return]    ${title}

get infodialog header
    ${header}    WebAuto.BasePage.get infodialog header
    [Return]    ${header}

get infodialog message
    ${message}    WebAuto.BasePage.get infodialog message
    [Return]    ${message}

click infodialog button
    [Arguments]    ${buttonName}
    WebAuto.BasePage.action infodialog click button    ${buttonName}

get errordialog message
    ${error message}    WebAuto.BasePage.get errordialog message
    [Return]    ${error message}

click errordialog button
    [Arguments]    ${button name}
    WebAuto.BasePage.action errordialog click button    ${button name}
