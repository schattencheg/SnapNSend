@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"
set "SERVER_PORT=8080"
set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending POST request to the server...

REM Set default values
set "ENDPOINT=/v1/requests"
set "DATA={\"user\": null, \"n\": 1, \"prompt\": \"test search query\", \"mode\": \"sync\"}"

REM Get user input for server URL (with default)
set /p "INPUT_URL=Enter server URL (default: !SERVER_URL!): "
if not "!INPUT_URL!"=="" set "SERVER_URL=!INPUT_URL!"

REM Get user input for endpoint
set /p "ENDPOINT=Enter endpoint (default: !ENDPOINT!): "
if "!ENDPOINT!"=="" set "ENDPOINT=/"

REM Get user input for JSON data
set /p "DATA=Enter JSON data (default: !DATA!): "
if "!DATA!"=="" set "DATA={}"

REM Construct the full URL
set "FULL_URL=!SERVER_URL!!ENDPOINT!"

echo.
echo Sending POST request to: !FULL_URL!
echo With data: !DATA!
echo.

REM Send the POST request using curl
curl -X POST ^
     -H "Content-Type: application/json" ^
     -d "!DATA!" ^
     "!FULL_URL!"

echo.
echo.
echo Request completed.
pause