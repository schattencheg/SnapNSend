@echo off
setlocal enabledelayedexpansion

echo Listing all processes related to the SnapNSend application...

echo.
echo === Processes listening on port 8000 ===
for /f "tokens=5" %%a in ('netstat -aon ^| findstr "LISTENING" ^| findstr :8000') do (
    set "PID=%%a"
    if not "!PID!"=="" if not "!PID!"=="0" (
        echo Process on port 8000: !PID!
    )
)

echo.
echo === Python processes with uvicorn in command line ===
for /f "skip=1" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn%%'" get ProcessId') do (
    if not "%%i"=="" if not "%%i"=="ProcessId" (
        echo PID: %%i
    )
)

echo.
echo === All Python processes ===
tasklist /fi "imagename eq python.exe" /v

echo.
echo === Active network connections ===
netstat -an | findstr "LISTENING"

echo.
echo Would you like to kill all Python processes? (y/n)
set /p answer="Enter choice: "

if /i {%answer%}=={y} (
    echo.
    echo Killing all Python processes...
    taskkill /f /im python.exe
    if !ERRORLEVEL! EQU 0 (
        echo All Python processes killed successfully.
    ) else (
        echo No Python processes were running or failed to kill them.
    )
) else (
    echo Skipping Python process termination.
)

echo.
pause