@echo off
setlocal enabledelayedexpansion

echo Sending POST request to the server...

REM Set default values
set "SERVER_URL=http://127.0.0.1:8000"
set "ENDPOINT=/v1/health"
set "FULL_URL=!SERVER_URL!!ENDPOINT!"
set "DATA={}"

REM Send request using curl
curl -X GET ^
     -H "Content-Type: application/json" ^
     -d "!DATA!" ^
     "!FULL_URL!"

echo.
echo.
echo Request completed.
pause