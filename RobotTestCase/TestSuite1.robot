*** Settings ***
Suite Setup       Login
Suite Teardown    WebAuto.Base.quit_browser
Library           WebAuto.LoginPage    ${browser}
Library           Selenium2Library
Library           WebAuto.MenuBar    ${browser}
Library           WebAuto.SearchPage    ${browser}
Library           WebAuto.Base    ${browser}
Resource          BasePageWrapper.robot
Library           WebAuto.ReportPage    ${browser}
Resource          UserKeywords.robot

*** Test Cases ***
MenuDemo
    action toggle menu
    sleep    1
    action expand app group    Supply Chain Advantage
    action expand menu    Advantage Dashboard
    action expand menu    Receiving
    action expand menu    ASNs    ${false}
    sleep    3
    action toggle menu
    sleep    1
    action collapse menu    Advantage Dashboard
    action expand menu    Receiving
    action collapse menu    Supply Chain Advantage
    action backto menu

search page
    action expand app group    Supply Chain Advantage
    action expand menu    Advantage Dashboard
    action expand menu    searchTest    ${false}    search test
    ${pagetitle}    get page title
    log    ${pagetitle}
    should be equal    ${pagetitle}    search test
    @{labelnames}    get all labels name
    log many    @{labelnames}
    action listbox select    ListBox    Warehouse 02    ${2}
    action checkbox check    checkbox2    ${2}
    action dropdown input    time    1:30 AM    ${2}
    action toggle menu
    sleep    1
    action expand menu    Inventory
    action expand menu    Inventory Snapshot    ${false}    Inventory Snapshot
    click page button    Create Snapshot
    ${errormessage}    get errordialog message
    log    ${errormessage}
    click errordialog button    Dismiss

report page
    action toggle menu
    sleep    1
    action collapse menu    Supply Chain Advantage
    action expand menu    Advantage Dashboard
    action expand menu    Receiving
    action expand menu    ASNs    ${false}    Search ASNs
    action dropdown select    Warehouse ID    Warehouse2 - Warehouse 02
    action searchlike input    ASN Number    ASN2
    click button    Query
    wait page    ASNs
    ${title}    get page title
    log    ${title}
    @{values}    get values by row    ${1}
    log many    @{values}
    action cell click    ${1}    ${1}
    @{rowtitle}    get rowdetail titles
    action extend rowdetail    @{rowtitle}[0]
    @{headers}    get headers    ASN DETAILS
    @{detailValues}    get values by row    ${1}    ASN DETAILS
    log many    @{headers}
    log many    @{detailValues}
    action cell click    ${1}    ${1}    ASN DETAILS
