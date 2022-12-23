*** Settings ***
Resource  resource.robot
Suite Setup  Open Browser And Reset Database
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***

Add And View Citation After Registering
    Go To Register Page
    Set Username  innokas_lukija
    Set Password  salasana123
    Set Password Confirmation  salasana123
    Submit Credentials
    Choose Book
    Input Citation Info  Herra Hakkarainen  Mauri Kunnas  2001
    Submit Citation
    Page Should Contain  Herra Hakkarainen

Cannot Add Citation With Letters As Year
    Choose Book
    Input Citation Info  Herra Hakkaraisen aakkoset  Mauri Kunnas  NollaNolla
    Submit Citation
    Page Should Not Contain  Herra Hakkaraisen aakkoset

Two Authors Are Arranged Correctly When New Citation Added
    Choose Book
    Input Citation Info  Herra Hakkarainen2  Sauli Niinistö;Mauri Kunnas  2001
    Submit Citation
    Page Should Contain  Mauri Kunnas, Sauli Niinistö
    Delete Citation

Multiple Authors Are Arranged Correctly When New Citation Added
    Choose Book
    Input Citation Info  Herra Hakkarainen3  Sauli Niinistö;Mauri Kunnas;Mato matala  2001
    Submit Citation
    Page Should Contain  Mauri Kunnas, Mato matala, Sauli Niinistö
    Delete Citation

Multiple Authors Are Arranged Correctly When Citation Modified
    Choose Book
    Input Citation Info  Herra Hakkarainen3  Sauli Niinistö;Mauri Kunnas  2001
    Submit Citation
    Modify Citation  
    Modify Authors  Sauli Niinistö;Mauri Kunnas;Mato matala
    Confirm Modification
    Page Should Contain  Mauri Kunnas, Mato matala, Sauli Niinistö
    Delete Citation

Modify Citation With Valid Inputs
    ModiFy Citation
    Modify Title  Herra Hakkarainen reissussa
    Confirm Modification
    Page Should Contain  Herra Hakkarainen reissussa

Modify Citation With Invalid Inputs
    ModiFy Citation
    Modify Year  NotInteger
    Confirm Modification
    Page Should Not Contain  NotInteger

Delete Citation
    Delete Citation
    Page Should Not Contain  Herra Hakkarainen reissussa
    Log Out

*** Keywords ***

Input Citation Info
    [Arguments]  ${title}  ${author}  ${year}
    Input text  title  ${title}
    Input text  author  ${author}
    Input text  year  ${year}

Submit Citation
    Click Button  Lisää viite

Choose Book
    Click Button  Kirja

Choose Article
    Click Button  Artikkeli

Delete Citation
    Click Button  Poista

ModiFy Citation
    Click Button  Muokkaa

Confirm Modification
    Click Button  Vahvista muokkaus

Modify Title
    [Arguments]  ${title}
    Input text  title  ${title}

Modify Authors
    [Arguments]  ${authors}
    Input text  author  ${authors}

Modify Year
    [Arguments]  ${year}
    Input text  year  ${year}
