import subprocess
import sys
import os
import time
import threading
import re

BASE = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE, ".venv", "Scripts", "python.exe")
CLOUDFLARED = os.path.join(os.environ["TEMP"], "cloudflared.exe")
APP_PY = os.path.join(BASE, "app.py")
FLASK_LOG = os.path.join(BASE, "flask_out.log")
TUNNEL_LOG = os.path.join(os.environ["TEMP"], "tunnel_url.log")

def start_flask():
    with open(FLASK_LOG, "w") as f:
        proc = subprocess.Popen(
            [VENV_PYTHON, APP_PY],
            cwd=BASE,
            stdout=f,
            stderr=subprocess.STDOUT
        )
    return proc

def start_tunnel():
    with open(TUNNEL_LOG, "w") as f:
        proc = subprocess.Popen(
            [CLOUDFLARED, "tunnel", "--url", "http://localhost:5000"],
            stdout=f,
            stderr=subprocess.STDOUT
        )
    return proc

print("Starting Flask...", flush=True)
flask_proc = start_flask()
time.sleep(3)

# Verify Flask is running
import urllib.request
for i in range(10):
    try:
        r = urllib.request.urlopen("http://localhost:5000/api/domains", timeout=3)
        print(f"Flask is UP (status {r.status})", flush=True)
        break
    except Exception:
        if i < 9:
            time.sleep(2)
        else:
            print("Flask failed to start", flush=True)
            flask_proc.kill()
            sys.exit(1)

print("Starting Cloudflare Tunnel...", flush=True)
tunnel_proc = start_tunnel()

# Wait for tunnel URL
url_pattern = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
for i in range(30):
    time.sleep(2)
    try:
        with open(TUNNEL_LOG, "r") as f:
            content = f.read()
        match = url_pattern.search(content)
        if match:
            url = match.group(0)
            print(f"\nTUNNEL_URL={url}", flush=True)
            # Keep running to maintain the tunnel
            print("Services running. Press Ctrl+C to stop.", flush=True)
            # Update the app's home URL
            main_activity = os.path.join(BASE, "android", "TrendScope", "app", "src", "main", "java", "com", "trendscope", "app", "MainActivity.kt")
            if os.path.exists(main_activity):
                with open(main_activity, "r") as f:
                    kotlin_code = f.read()
                kotlin_code = re.sub(
                    r'val HOME_URL = "https://[^"]+"',
                    f'val HOME_URL = "{url}"',
                    kotlin_code
                )
                with open(main_activity, "w") as f:
                    f.write(kotlin_code)
                print(f"Updated HOME_URL in MainActivity.kt to {url}", flush=True)
            import webbrowser
            webbrowser.open(url)
            print(f"Opened {url} in browser", flush=True)
            # Keep running
            try:
                while True:
                    time.sleep(10)
                    # Check both process are alive
                    if flask_proc.poll() is not None:
                        print("Flask process died!", flush=True)
                        break
                    if tunnel_proc.poll() is not None:
                        print("Tunnel process died!", flush=True)
                        break
            except KeyboardInterrupt:
                pass
            break
    except FileNotFoundError:
        pass
    print(f"Waiting for tunnel... ({i+1}/30)", flush=True)

print("Shutting down...", flush=True)
flask_proc.kill()
tunnel_proc.kill()
