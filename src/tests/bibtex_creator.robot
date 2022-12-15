*** Settings ***
Resource  resource.robot
Suite Setup  Open Browser And Reset Database
Suite Teardown  Close Browser
Test Setup  Go To Main Page First

*** Test Cases ***

Add Book Adds Entry to Bibtex
    Reset Database First
    Go To Register Page
    Set Username  nimi
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Set Title  kirja
    Set Author  kirjailija
    Set Year  1999
    Submit Entry
    Inspect Bibtex
    page Should Contain  author = "kirjailija", title = "kirja", year = "1999"

*** Keywords ***

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password1  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password2  ${password}

Set Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Author
    [Arguments]  ${author}
    Input Text  author  ${author}

Set Year
    [Arguments]  ${year}
    Input Text  year  ${year}

Reset Database First
    Reset Database

Submit Credentials
    Click Button  Luo tunnus

Submit Entry
    Click Button  Lisää viite

Go To Register Page
    Click Link  Luo uusi tunnus

Go To Main Page First
    Go To Main Page

Inspect Bibtex
    Click Element  Tarkastele
