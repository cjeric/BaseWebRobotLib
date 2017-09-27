*** Settings ***
Library           WebAuto.MenuBar    ${browser}

*** Keywords ***
NaviToPage
    [Arguments]    @{menus}
    action toggle menu
