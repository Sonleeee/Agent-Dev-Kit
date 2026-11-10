@echo off
REM Launcher for Chrome with Remote Debugging Port 9222
REM Uses the REAL Chrome profile so logins, cookies and extensions persist.

set CHROME_PATH=""
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set CHROME_PATH="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if %CHROME_PATH%=="" (
    echo [ERROR] Google Chrome not found.
    pause
    exit /b 1
)

echo ========================================================
echo [INFO] Khởi động Chrome với cổng Debug 9222
echo [INFO] Dùng session thật của tài khoản (Default profile)
echo ========================================================
echo Lưu ý: Hãy đóng các cửa sổ Chrome cũ trước khi chạy lệnh này
echo để Chrome mở được cổng 9222 trên Profile chính.
echo.

start "" %CHROME_PATH% --remote-debugging-port=9222

echo [SUCCESS] Chrome đã khởi động tại http://localhost:9222
