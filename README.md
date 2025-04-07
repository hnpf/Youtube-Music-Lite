YT Music Lite - Unofficial (Python)

This is a simple Python application that allows you to browse and stream music from YouTube Music using PyQt5 and a custom web engine. It's lightweight and provides a convenient interface to access YouTube Music without the need for a full web browser.
Features

    Browse YouTube Music

    Hide login elements from the interface

    Open login requests in your system's default web browser

    Customizable profile for storing session data

    Basic web view UI

Requirements

    Python 3.x

    PyQt5 for the GUI and web engine interaction

    re for regular expressions (built-in Python module)

Install the required dependencies:

pip install PyQt5 --thats literally everything

Usage

The app will open a PyQt5 window with the YouTube Music site loaded. The UI will hide login elements, and any login requests will open in your default browser.
Customize

    You can change the url variable to load a different web page if needed. Hell, even make your own web app with it, idc 

    Modify the app's user agent or cookies handling by editing the profile.setHttpUserAgent and profile.setPersistentCookiesPolicy settings in the code <3

How It Works

    The app uses QWebEngineView from PyQt5 to load the YouTube Music website.

    A custom QWebEnginePage class intercepts navigation requests to avoid logging in within the app itself.

    Login requests are redirected to your system's default web browser.

    Some login elements on the site are hidden using JavaScript injection to avoid clutter.

License

this project isnt licensed, do what you want, its free, just dont do anything illegal with it :)
