@echo off

REM Windows script for running unit tests
REM You have to run server and capture some browser first
REM
REM Requirements:
REM - NodeJS (http://nodejs.org/)
REM - Testacular (npm install -g testacular)

REM set CHROME_BIN="c:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
echo %CHROME_BIN%
set BASE_DIR=%~dp0
testacular start "%BASE_DIR%\..\config\testacular.conf.js" --start-maximized
