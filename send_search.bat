@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"

REM Use environment variable for server port, default to 9000 if not set
set "SERVER_PORT=%SERVER_PORT%"
if "!SERVER_PORT!"=="" set "SERVER_PORT=9000"

set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending POST request to the server...

SET "id=c5d8e386-bce7-40db-9051-90a1aed46045"

REM Set default values
set "ENDPOINT=/v1/requests"
set "DATA={\"user\": \"!id!\", \"n\": 1, \"prompt\": \"test search query\", \"mode\": \"sync\"}"

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