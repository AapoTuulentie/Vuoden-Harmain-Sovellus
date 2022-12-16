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
    Click Button  Kirja
    Set Title   Kyberias 
    Set Author   Stanislaw Lem 
    Set Year   1999 
    Set Citekey   oma viite 
    Submit Entry
    Execute JavaScript  window.scrollTo(0,2000)
    Inspect Bibtex
    Switch Window  .bib
    Page Should Contain  Stanislaw Lem  
    Page Should Contain  Kyberias 
    Page Should Contain  1999  
    Page Should Contain  oma viite   
    Switch Window  Otsikko
    Go To Main Page

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

Set Citekey
    [Arguments]  ${citekey}
    Input Text  citekey  ${citekey}

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
    Click Link  Tarkastele bib-tiedostoa
