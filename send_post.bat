@echo off
setlocal enabledelayedexpansion

REM Load configuration
set "PROJECT_DIR=%~dp0"
set "SERVER_PORT=8080"
set "SERVER_URL=http://127.0.0.1:!SERVER_PORT!"

echo Sending POST request to the server...

REM Set default values
set "ENDPOINT=/v1/requests"  REM Changed to a common endpoint name
set "DATA={\"user\": null, \"n\": 1, \"prompt\": \"test search query\", \"mode\": \"sync\"}"

REM Show example
echo Example: POST to /v1/requests endpoint with sample data
echo Server URL: !SERVER_URL!
echo Endpoint: !ENDPOINT!
echo Sample JSON data: !DATA!
echo.

REM Get user input for server URL (with default)
set /p "INPUT_URL=Enter server URL (default: !SERVER_URL!): "
if not "!INPUT_URL!"=="" set "SERVER_URL=!INPUT_URL!"

REM Get user input for endpoint
set /p "ENDPOINT=Enter endpoint (default: !ENDPOINT!): "
if "!ENDPOINT!"=="" set "ENDPOINT=/v1/requests"

REM Get user input for JSON data
echo Enter JSON data (use double quotes and escape them, or press Enter for default):
set /p "DATA_INPUT="
if not "!DATA_INPUT!"=="" set "DATA=!DATA_INPUT!"

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