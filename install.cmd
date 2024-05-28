@echo off
setlocal enabledelayedexpansion

REM Change the file path to the location of your text file
set "file_path=./requirements.txt"

REM Check if the file exists
if not exist "%file_path%" (
    echo File does not exist!
    exit /b
)

REM Read each line of the text file and run pip install command with each line
for /f "tokens=*" %%a in ('type "%file_path%"') do (
    echo Installing package: %%a
    pip install %%a
)

pause
