*** Settings ***
Resource  resource.robot
Suite Setup  Open Browser And Reset Database
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***

Add And View Citation After Registering
    Go To Register Page
    Set Username  kayttaja1
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Input Citation Info  Herra Hakkarainen  Mauri Kunnas  2001
    Submit Citation
    Page Should Contain  Herra Hakkarainen

Cannot Add Citation With Letters As Year
    Input Citation Info  Herra Hakkaraisen aakkoset  Mauri Kunnas  NollaNolla
    Submit Citation
    Page Should Not Contain  Herra Hakkaraisen aakkoset

Modify Citation With Valid Inputs
    ModiFy Citation
    Modify Title  Nimi
    Confirm Modification
    Page Should Contain  Nimi

Modify Citation With Invalid Inputs
    ModiFy Citation
    Modify Year  NotInteger
    Confirm Modification
    Page Should Not Contain  NotInteger

Delete Citation
    Delete Citation
    Page Should Not Contain  Nimi
    Log Out

*** Keywords ***

Input Citation Info
    [Arguments]  ${title}  ${author}  ${year}
    Input text  title  ${title}
    Input text  author  ${author}
    Input text  year  ${year}

Submit Citation
    Click Button  Lisää viite

Delete Citation
    Click Button  Poista

ModiFy Citation
    Click Button  Muokkaa

Confirm Modification
    Click Button  Vahvista muokkaus

Modify Title
    [Arguments]  ${title}
    Input text  title  ${title}

Modify Year
    [Arguments]  ${year}
    Input text  year  ${year}
