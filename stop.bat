@echo off
setlocal enabledelayedexpansion

echo Stopping uvicorn server...

REM Define project directory
set "PROJECT_DIR=G:\Work\Repos\stagee_2026_01\SnapNSend"

REM Check if PID file exists
if not exist "!PROJECT_DIR!\uvicorn.pid" (
    echo PID file not found. Attempting to stop server by other methods...
    goto :alternative_stop
)

REM Read the stored PID
set "PID="
for /f "usebackq" %%i in ("!PROJECT_DIR!\uvicorn.pid") do set "PID=%%i"

REM Check if PID was read successfully
if "!PID!"=="" (
    echo Could not read PID from file. Attempting alternative methods...
    goto :alternative_stop
)

echo Found stored PID: !PID!

REM Kill the process using the stored PID
taskkill /f /t /pid !PID! 2>nul
if !ERRORLEVEL! EQU 0 (
    echo Uvicorn server with PID !PID! stopped successfully.
    REM Clean up the PID file
    del "!PROJECT_DIR!\uvicorn.pid" 2>nul
    goto :verify_server
) else (
    echo Failed to stop process with PID !PID!. It may have already been terminated.
    REM Clean up the PID file anyway
    del "!PROJECT_DIR!\uvicorn.pid" 2>nul
    goto :verify_server
)

:alternative_stop
REM Alternative method: Kill by port
echo Looking for processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr LISTENING ^| findstr :8000') do (
    set "PID=%%a"
    if not "!PID!"=="" if not "!PID!"=="0" (
        echo Found process on port 8000: !PID!
        taskkill /f /t /pid !PID! 2>nul
        if !ERRORLEVEL! EQU 0 (
            echo Uvicorn server stopped successfully.
        )
        goto :verify_server
    )
)

REM Alternative method: Kill by command line
echo Looking for Python processes with uvicorn in command line...
for /f "skip=1 tokens=1" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn app.main%%'" get ProcessId') do (
    set "PID=%%i"
    if not "!PID!"=="" if not "!PID!"=="0" if not "!PID!"=="ProcessId" (
        echo Found uvicorn process: !PID!
        taskkill /f /t /pid !PID! 2>nul
        goto :verify_server
    )
)

echo No uvicorn processes found or already stopped.

:verify_server
echo.
echo Waiting for connections to close...
timeout /t 3 /nobreak >nul

REM Test if localhost:8000 is accessible using curl (if available) or PowerShell
echo Testing localhost:8000 connectivity...

REM Try using curl first (more reliable)
curl --connect-timeout 3 --max-time 5 http://127.0.0.1:8000 >nul 2>&1
set CURL_RESULT=%ERRORLEVEL%

if %CURL_RESULT% EQU 0 (
    echo WARNING: Server is still accessible at http://127.0.0.1:8000
    echo The server may not have stopped completely.
) else (
    REM If curl is not available or returns error, try PowerShell
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000' -TimeoutSec 3 -UseBasicParsing; exit 1 } catch { exit 0 }"
    set POWERSHELL_RESULT=!ERRORLEVEL!
    
    if !POWERSHELL_RESULT! EQU 1 (
        echo WARNING: Server is still accessible at http://127.0.0.1:8000
        echo The server may not have stopped completely.
    ) else (
        echo SUCCESS: Server is no longer accessible at http://127.0.0.1:8000
        echo The server has been successfully stopped.
    )
)

echo.
pause