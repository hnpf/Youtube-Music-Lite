@echo off
setlocal enabledelayedexpansion

set "INSTALL_DIR=%APPDATA%\YTM-Music"

echo Uninstalling YTM-Music from %INSTALL_DIR%...

if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo Removed installation directory.
) else (
    echo Installation directory not found.
)

echo Removing desktop shortcut...
del "%USERPROFILE%\Desktop\YTM-Music.lnk" 2>nul

echo Uninstallation complete!
pause