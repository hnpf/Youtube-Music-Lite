# YouTube Music Lite

Chromshitum based, portable launcher for YouTube Music using Chromshitum. this opens ytm in a window with built in adblocking via uBlock Origin. - Doesnt work correctly for Windows.

-Note, This doesnt INCLUDE /oss/ and the files inside of it. due to copyright and other reasons, you should use this as a template for yourself!
## features

- **portable Chromshitum build**: Uses a portable version of Chromshitum for Windows and Linux.
- **adblocking**: uses uBlock Origin.
- **profiles**: uses separate profiles for the app to avoid interfering with your default browser.
- **cross-platform**: windows and linux support.

## requirements

- **python 3**: needed to run the launcher script.
- **portable Chromshitum**: included in the `oss/` directory for windows (`WindowsChromium`) and linux (`LinuxChromium`).

## install

### for windows

1. run `install.bat`.
2. it will:
   - copy all files to `%APPDATA%\YTM-Music`.
   - and create a desktop shortcut named `YTM-Music.lnk`.
3. optional, simply dont install and run python script directly. best route is portable.

### linux

1. python 3 is installed.
2. open `python3 ym_music.py` from the project directory.
3. the script will handle copying uBlock Origin to the profile if needed.

## using

- **launching**: simply run the script to open YouTube Music in a Chromshitum window.
- **profiles**: user data is stored in `~/.ytm-lite-profiles/music_youtube_com` to keep it separate from your main browser.

### commandline options

script can be customized by modifying `ym_music.py`:

- `url`: change the default URL (default: `https://music.youtube.com`). basically this can also work for any other sites.
- `debug`: enable/disable debug logging (default: `True`).
- `persist`: whether to persist the profile (default: `True`).

## remove

### for windows

1. simply `uninstall.bat`.
2. it will remove the installation directory and desktop shortcut.
3. if needed, simply delete the portable folder too.

### linux

1. delete the project directory and the profile folder (`~/.ytm-lite-profiles`). that easy!

## for troubleshooting

- **Chromshitum not found**: make sure the portable Chromshitum executable is in the correct path (`oss/WindowsChromium/app/chrome.exe` for Windows, `oss/LinuxChromium/UGChrome.appimage` for Linux).
- **uBlock not loading**: Check if the uBlock extension files are present in the `oss/` directory. if on windows, its not supported. its almost guaranteed to work for linux.
- **any permission issues**: on linux, make sure the script has execute permissions by: `chmod +x ym_music.py`.
- **python path**: make sure `python` or `python3` is in your PATH.

## contributing

feel free to fork and submit pull requests. try to make sure changes are compatible with both windows and linux!

## license

this project is open-source. Check the license file for details.

## disclaimer


this tool is for personal use. respect and follow youtube's terms of service.

