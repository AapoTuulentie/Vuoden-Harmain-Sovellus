*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.0 seconds
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

<<<<<<< HEAD
Bibtex Should Contain
    Page Should Contain  @Book{None, author = "kirjailija", title = "Otsikko", year = "1999", }

=======
Log Out
    Click Link  Kirjaudu ulos

Submit Credentials
    Click Button  Luo tunnus

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
>>>>>>> 2540d8e4db0cacfd474ba0d068c71222ef13d98c
