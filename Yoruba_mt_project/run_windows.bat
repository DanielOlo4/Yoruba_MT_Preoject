@echo off
setlocal
cd /d "%~dp0"
title Yoruba-English Translation System

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON=py"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo.
        echo Python was not found on this computer.
        echo Install Python from https://www.python.org/downloads/ and try again.
        pause
        exit /b 1
    )
    set "PYTHON=python"
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating the project environment. Please wait...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto :error
)

echo Checking required packages...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Starting the Yorùbá-English Translation System...
echo The website will open at http://127.0.0.1:5000
start "" /b powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5000'"
.venv\Scripts\python.exe app.py

echo.
echo The server has stopped.
pause
exit /b 0

:error
echo.
echo The application could not start. Review the message above.
pause
exit /b 1
