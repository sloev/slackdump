import subprocess
import json
from contextlib import contextmanager
import time
import requests
import logging


@contextmanager
def osx_chrome(port=9999):
    get_browser_bundle_id = "cat ~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist | plutil -convert json -r -o - -- -"
    json_string = subprocess.check_output(get_browser_bundle_id, shell=True)
    json_data = json.loads(json_string)
    browser_bundle_id = [
        e for e in json_data["LSHandlers"] if e.get("LSHandlerURLScheme") == "http"
    ][0]["LSHandlerRoleAll"]
    browser_app_path = (
        f"/usr/bin/defaults read {browser_bundle_id} LastRunAppBundlePath"
    )
    browser_path = (
        subprocess.check_output(browser_app_path, shell=True).strip().decode("utf-8")
    )
    browser_path = f"{browser_path}/Contents/MacOS/{browser_path.rsplit('.app', 1)[0].rsplit('/', 1)[1]}".replace(
        " ", "\ "
    )
    headless_chrome_process = (
        f"{browser_path} --remote-debugging-port={port}"
    )
    try:
        proc = subprocess.Popen(headless_chrome_process, stderr=subprocess.PIPE, shell=True)
        debug_url = None
        for i in range(50):
            line = proc.stderr.readline().decode('utf-8').lower()
            if 'devtools listening on ' in  line:
                debug_url = line.split('devtools listening on ', 1)[1].strip()
                logging.warning(f"Found debug url: '{debug_url}'")
                break
        if debug_url is None:
            raise ValueError('couldnt figure out debug_url')
        time.sleep(5)
        yield debug_url
    finally:
        try:
            proc.kill()
        except:
            pass
