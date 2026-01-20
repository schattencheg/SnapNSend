@echo off
setlocal enabledelayedexpansion

echo Sending POST request to the server...

REM Set default values
set "SERVER_URL=http://127.0.0.1:8000"
set "ENDPOINT=/v1/register"
set "FULL_URL=!SERVER_URL!!ENDPOINT!"
set "DATA={\"user_name\": \"schattencheg\", \"user_mail\": \"schattencheg@gmail.com\"}"

REM Send request using curl
curl -X POST ^
     -H "Content-Type: application/json" ^
     -d "!DATA!" ^
     "!FULL_URL!"

echo.
echo.
echo Request completed.
pause