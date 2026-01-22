@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"
set "SERVER_PORT=8080"
set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending POST request to the server register endpoint...

REM Set default values
set "ENDPOINT=/v1/register"
set "FULL_URL=!SERVER_URL!!ENDPOINT!"
set "DATA={\"user_name\": \"test_user\", \"user_mail\": \"test@example.com\"}"

REM Send request using curl
curl -X POST ^
     -H "Content-Type: application/json" ^
     -d "!DATA!" ^
     "!FULL_URL!"

echo.
echo.
echo Request completed.
pause