import subprocess, sys, time, os, re, signal

dir = r"PROJECT_ROOT"
venv_python = os.path.join(dir, ".venv", "Scripts", "python.exe")
cloudflared = os.path.join(os.environ["TEMP"], "cloudflared.exe")
tunnel_log = os.path.join(dir, "tun3.log")

# Start Flask
flask_proc = subprocess.Popen(
    [venv_python, "app.py"],
    cwd=dir,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
)
print("Flask PID:", flask_proc.pid)
time.sleep(4)

# Start cloudflared
with open(tunnel_log, "w") as f:
    tun_proc = subprocess.Popen(
        [cloudflared, "tunnel", "--url", "http://localhost:5000"],
        stdout=f,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
print("Tunnel PID:", tun_proc.pid)

# Wait for tunnel URL
time.sleep(10)
with open(tunnel_log, "r") as f:
    content = f.read()

match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
if match:
    url = match.group(0)
    print("URL:", url)

    # Verify it works
    import requests
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=10)
            print("Status:", r.status_code, len(r.text), "bytes")
            if r.status_code == 200:
                print("OK!")
                break
        except Exception as e:
            print("Attempt", attempt+1, "failed:", e)
        time.sleep(3)
else:
    print("No URL found in tunnel log")
    print("Log last 30 lines:")
    lines = content.strip().split("\n")
    for l in lines[-30:]:
        print(" ", l)

print("Processes running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    flask_proc.terminate()
    tun_proc.terminate()
    print("Stopped")
