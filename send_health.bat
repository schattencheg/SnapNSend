@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"
set "SERVER_PORT=8080"
set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending GET request to the server health endpoint...

REM Set default values
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