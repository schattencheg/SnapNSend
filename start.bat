@echo off
setlocal enabledelayedexpansion

REM Store the current directory
set "PROJECT_DIR=%~dp0"
set "MAIN_DIR=!PROJECT_DIR!\main"
set "VENV_DIR=!PROJECT_DIR!\venv"
set "SERVER_PORT=8080"

REM Activate virtual environment
if exist "!VENV_DIR!\Scripts\activate.bat" (
    call "!VENV_DIR!\Scripts\activate.bat"
    echo Virtual environment activated.
) else (
    echo Warning: Virtual environment not found at !VENV_DIR!
    echo Using system Python installation.
)

cd /d "!MAIN_DIR!"

echo Starting uvicorn server...

REM Try to start the server with a higher port that doesn't require admin privileges
echo Attempting to start server on port !SERVER_PORT! (requires no admin privileges)...
start "Uvicorn-Server" cmd /c "uvicorn app.main:app --host 127.0.0.1 --port !SERVER_PORT! --reload --log-level info && echo Server stopped. Press any key to close... && pause >nul"

REM Wait a moment for the server to start
timeout /t 5 /nobreak >nul

REM Find the PID of the newly started uvicorn process and save it
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn app.main:app%%' and commandline like '%%--port !SERVER_PORT!%%'" get ProcessId ^| findstr [0-9]') do (
    echo %%i > "!PROJECT_DIR!\uvicorn.pid"
    echo Uvicorn server started with PID: %%i
    goto :start_done
)

REM If we couldn't get the exact PID, try to find any recent uvicorn process
for /f "skip=1 tokens=1" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn%%'" get ProcessId') do (
    if not "%%i" == "" (
        echo %%i > "!PROJECT_DIR!\uvicorn.pid"
        echo Started uvicorn server (approximate PID: %%i)
        goto :start_done
    )
)

:start_done
cd /d "!PROJECT_DIR!"
echo Server should be available at http://127.0.0.1:!SERVER_PORT!
echo Note: If server fails to start, you may need to run this script as Administrator
echo or check Windows Firewall/Antivirus settings for port restrictions.
pause