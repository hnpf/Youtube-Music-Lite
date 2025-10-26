@echo off
setlocal enabledelayedexpansion

set "INSTALL_DIR=%APPDATA%\YTM-Music"
set "SOURCE_DIR=%~dp0"

echo Installing YTM-Music to %INSTALL_DIR%...

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

xcopy "%SOURCE_DIR%*" "%INSTALL_DIR%\" /E /I /Y

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\YTM-Music.lnk'); $Shortcut.TargetPath = 'python.exe'; $Shortcut.Arguments = '\"%INSTALL_DIR%\ym_music.py\"'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\oss\WindowsChromium\app\chrome.exe,0'; $Shortcut.Save()"

echo Installation complete! Shortcut created on desktop.
pause