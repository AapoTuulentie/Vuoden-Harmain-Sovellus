*** Settings ***
Resource  resource.robot
Suite Setup  Open Browser And Reset Database
Suite Teardown  Close Browser
Test Setup  Go To Main Page First


*** Test Cases ***
Register With Valid Username And Password
    Reset Database First
    Go To Register Page
    Set Username  nimi
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Register Should Succeed
    Log Out

Can not Register With Too Short Username
    Reset Database First
    Go To Register Page
    Set Username  ni
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Register Should Fail

Can not Register With Too Short Password
    
    Go To Register Page
    Set Username  nimi
    Set Password  sa
    Set Password Confirmation  sa
    Submit Credentials
    Register Should Fail

Can not Register With Password Mismatch
    Go To Register Page
    Set Username  nimi
    Set Password  salasana123
    Set Password Confirmation  salaminaama123
    Submit Credentials
    Register Should Fail With Message  Salasanat eivät ole samat

Registered User Should Be Able To Log In
    Reset Database First

    Go To Register Page
    Set Username  nimi1  
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Log Out
    Set Username  nimi1
    Set Password Main Page  salasana123
    Log In
    Log In Should Succeed 
    Log Out

Log In Should Not Work With Incorrect Credentials
    Reset Database First

    Set Username  hakkeripahis
    Set Password Main Page  salasana123
    Log In
    Log In Should Fail With Message  Väärä käyttäjätunnus tai salasana 

Logging Out Redirects To Main Page
    Reset Database First
    Go To Register Page
    Set Username  nimi1  
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Log Out
    Main Page Should Be Open

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password1  ${password}

Set Password Main Page
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password2  ${password}

Submit Credentials
    Click Button  Luo tunnus

Go To Main Page First
    Go To Main Page

Go To Register Page
    Click Link  Luo uusi tunnus

Register Should Succeed
    Main Page Should Be Open

Register Should Fail
    Register Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Page Should Contain  ${Message}

Login Should Fail With Message
    [Arguments]  ${message}
    Page Should Contain  ${Message}

Log Out
    Click Link  Kirjaudu ulos

Log In
    Click Button  Kirjaudu

Log In Should Succeed
    Main Page Should Be Open

Reset Database First
    Reset Database