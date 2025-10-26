#!/usr/bin/env python3
# ytm-lite — portable chromium edition, uBlock only forced on linux

import os, sys, platform, shutil, subprocess, signal
from pathlib import Path

class BrowserAppLauncher:
    def __init__(self, url="https://music.youtube.com", debug=True, persist=True):
        self.url = url
        self.debug = debug
        self.persist = persist
        self.process = None
        self.system = platform.system()

        self._log("init:", self.url)

        # profile dir
        self.base_profile = Path.home() / ".ytm-lite-profiles"
        self.base_profile.mkdir(parents=True, exist_ok=True)
        app_name = self.url.split("://")[-1].split("/")[0].replace(".", "_")
        self.profile_path = self.base_profile / app_name
        self.profile_path.mkdir(exist_ok=True)

        # optional uBlock
        self.ublock_path = None
        self.ublock_id = "cjpalhdlnbpafiamejdnhcphjbkeiagm"  # uBlock Origin ID
        if self.system == "Windows":
            # Use built-in uBlock for Windows
            source_ublock = Path("./oss/WindowsChromium/app/Extensions/uBlock0.chromium")
            if source_ublock.exists() and source_ublock.is_dir():
                self.ublock_path = source_ublock
                self._log("using uBlock from", source_ublock)
            else:
                self._log("no uBlock found, skipping")
        else:
            # For Linux, copy uBlock to profile
            self.extensions_dir = self.base_profile / "music_youtube_com/extensions"
            self.extensions_dir.mkdir(parents=True, exist_ok=True)
            source_ublock = Path("./oss/LinuxChromium/uBlock0.chromium")
            target_ublock = self.extensions_dir / "uBlock0.chromium"
            if source_ublock.exists() and source_ublock.is_dir():
                if not target_ublock.exists():
                    shutil.copytree(source_ublock, target_ublock)
                    self._log("uBlock copied to", target_ublock)
                else:
                    self._log("uBlock already present")
                self.ublock_path = target_ublock
            else:
                self._log("no uBlock found, skipping")

        # pick portable chromium
        self.browser_path = self._get_portable_chromium()

    def _log(self, *a):
        if self.debug:
            print("[LOG]", *a)

    def _get_portable_chromium(self):
        if self.system == "Windows":
            path = Path("./oss/WindowsChromium/app/chrome.exe")
        elif self.system == "Linux":
            path = Path("./oss/LinuxChromium/UGChrome.appimage")
        else:
            raise OSError(f"{self.system} not supported for portable chromium")
        if not path.exists():
            raise FileNotFoundError(f"Portable chromium not found at {path}")
        self._log("using portable chromium at", path)
        return str(path)

    def launch(self):
        args = [
            self.browser_path,
            f"--app={self.url}",
            f"--user-data-dir={self.profile_path.resolve()}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking"
        ]

        if self.ublock_path:
            args.append(f"--enable-extensions")
            args.append(f"--load-extension={self.ublock_path.resolve()}")
            args.append(f"--disable-extensions-except={self.ublock_id}")

        self._log("launch args:", args)

        preexec = None
        creationflags = 0
        if self.system != "Windows":
            preexec = os.setsid
        else:
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        try:
            self.process = subprocess.Popen(
                args,
                stdout=None if self.debug else subprocess.DEVNULL,
                stderr=None if self.debug else subprocess.DEVNULL,
                preexec_fn=preexec,
                creationflags=creationflags
            )
            print("[+] browser launched pid", self.process.pid)
            return True
        except Exception as e:
            print("[!] failed to launch browser:", e)
            return False

    def wait(self):
        if not self.process:
            return
        try:
            print("[*] waiting for browser (ctrl+c to quit)..")
            self.process.wait()
        except KeyboardInterrupt:
            print("\n[!] keyboard interrupt, killing browser..")
            self.kill()

    def kill(self):
        if not self.process:
            return
        pid = self.process.pid
        self._log("killing pid", pid)
        try:
            if self.system == "Windows":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                               stdout=None if self.debug else subprocess.DEVNULL,
                               stderr=None if self.debug else subprocess.DEVNULL)
            else:
                import os, signal
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if self.system == "Windows":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)])
                else:
                    os.killpg(os.getpgid(pid), signal.SIGKILL)
            print("[x] browser terminated")
        except Exception as e:
            self._log("kill exception:", e)

    def run(self):
        if self.launch():
            self.wait()
            return 0
        return 1


def main():
    launcher = BrowserAppLauncher(debug=True, persist=True)

    def handler(sig, frame):
        print("\n[!] signal caught, shutting down..")
        launcher.kill()
        sys.exit(0)

    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(s, handler)
        except Exception:
            pass

    try:
        sys.exit(launcher.run())
    except Exception as e:
        print("[crash]", e)
        launcher.kill()
        sys.exit(1)


if __name__ == "__main__":
    main()
