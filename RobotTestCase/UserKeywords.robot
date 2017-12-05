*** Settings ***
Library           Collections
Library           WebAuto.CommonFunction.mail    ${user}    ${pwd}    ${smtp_server}

*** Keywords ***
MailTo
    [Arguments]    ${tolist}    ${body}    ${header}    ${attachment}=${None}
    send mail    ${tolist}    ${body}    ${header}    ${attachment}
