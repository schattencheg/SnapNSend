@echo off
setlocal enabledelayedexpansion

REM Store the current directory
set "PROJECT_DIR=G:\Work\Repos\stagee_2026_01\SnapNSend"
set "MAIN_DIR=!PROJECT_DIR!\main"

cd /d "!MAIN_DIR!"

echo Starting uvicorn server...

REM Start the server in a separate window and save the process info
start "Uvicorn-Server" cmd /c "uvicorn app.main:app --reload && pause"

REM Wait a moment for the server to start
timeout /t 5 /nobreak >nul

REM Find the PID of the newly started uvicorn process and save it
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn app.main:app%%' and creationdate >= '!date:~0,4!!date:~-4,2!!date:~-10,2%!000000.000000+000'" get ProcessId ^| findstr [0-9]') do (
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
echo Server should be available at http://127.0.0.1:8000
pause