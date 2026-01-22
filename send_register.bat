@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"

REM Use environment variable for server port, default to 9000 if not set
set "SERVER_PORT=%SERVER_PORT%"
if "!SERVER_PORT!"=="" set "SERVER_PORT=9000"

set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending POST request to the server register endpoint...

REM Set default values
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