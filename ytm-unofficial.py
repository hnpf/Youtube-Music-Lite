import sys
import webbrowser
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QUrl, pyqtSlot, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings
class CustomWebPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        try:
            self.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        except:
            pass
    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        url_str = url.toString()
        auth_domains = [
            r"accounts\.google\.com",
            r"youtube\.com/signin",
        ]
        for domain in auth_domains:
            if re.search(domain, url_str):
                print(f"Redirecting login request to system browser: {url_str}")
                webbrowser.open(url_str)
                return False
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)
    def javaScriptConsoleMessage(self, level, message, line, source):
        levels = ['Info', 'Warning', 'Error']
        if level > 0:
            print(f"JS {levels[min(level, 2)]} at line {line}: {message} (Source: {source})")
class WebsiteBrowser(QMainWindow):
    def __init__(self, url, app_name="Web Browser"):
        super().__init__()
        self.url = url
        self.app_name = app_name
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle(f"Loading {self.app_name}...")
        self.setGeometry(100, 100, 1200, 800)
        self.web_view = QWebEngineView()
        profile_path = QDir.homePath() + f"/.{self.app_name.lower().replace(' ', '_')}_profile"
        self.profile = QWebEngineProfile(profile_path, self.web_view)
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        self.page = CustomWebPage(self.profile, self.web_view)
        self.web_view.setPage(self.page)
        self.web_view.loadFinished.connect(self.page_loaded)
        self.web_view.loadProgress.connect(self.update_progress)
        self.setCentralWidget(self.web_view)
        self.web_view.load(QUrl(self.url))
    @pyqtSlot(bool)
    def page_loaded(self, success):
        if success:
            title = self.web_view.page().title()
            self.setWindowTitle(f"{title} - {self.app_name}")
            self.web_view.page().runJavaScript("""
                function hideLoginElements() {
                    const loginElements = document.querySelectorAll('[id*="login"], [class*="login-dialog"], [class*="sign-in"]');
                    loginElements.forEach(el => {
                        if (el) el.style.display = 'none';
                    });
                    setTimeout(hideLoginElements, 3000);
                }
                hideLoginElements();
            """)
        else:
            self.setWindowTitle(f"Error loading - {self.app_name}")
            QMessageBox.warning(self, "Load Error", f"Failed to load {self.url}")
    @pyqtSlot(int)
    def update_progress(self, progress):
        if progress < 100:
            self.setWindowTitle(f"Loading {self.app_name}... ({progress}%)")
def main():
    app_name = "YT Music lite - unofficial and made by hnpf on github."
    url = "https://music.youtube.com"
    app = QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setOrganizationName("YTMusic")
    browser = WebsiteBrowser(url, app_name)
    browser.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()