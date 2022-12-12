*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  chrome
${DELAY}  0.2 seconds
${HOME URL}  http://${SERVER}
${LOGIN URL}  http://${SERVER}/login
${REGISTER URL}  http://${SERVER}/register

*** Keywords ***
Open Browser And Reset Database
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}
    Reset Database

Login Page Should Be Open
    Title Should Be  Login

Register Page Should Be Open
    Title Should Be  Otsikko

Main Page Should Be Open
    Title Should Be  Otsikko

Go To Main Page
    Go To  ${HOME URL}

Go To Login Page
    Go To  ${LOGIN URL}

Go To Register Page
    Go To  ${REGISTER URL}

Bibtex Should Contain
    Page Should Contain  @Book{None, author = "kirjailija", title = "Otsikko", year = "1999", }

