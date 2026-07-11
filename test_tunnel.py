import subprocess, os, time, re, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE, ".venv", "Scripts", "python.exe")
CLOUDFLARED = os.path.join(os.environ["TEMP"], "cloudflared.exe")
TUNNEL_LOG = os.path.join(os.environ["TEMP"], "tunnel_url.log")

# Start Flask
flask_proc = subprocess.Popen([VENV_PYTHON, os.path.join(BASE, "app.py")], cwd=BASE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

# Test Flask locally
try:
    r = urllib.request.urlopen("http://localhost:5000/api/domains", timeout=5)
    print(f"Flask local: OK ({r.status})", flush=True)
except Exception as e:
    print(f"Flask local: FAILED - {e}", flush=True)
    flask_proc.kill()
    exit(1)

# Start tunnel
with open(TUNNEL_LOG, "w") as f:
    tunnel_proc = subprocess.Popen([CLOUDFLARED, "tunnel", "--url", "http://localhost:5000"], stdout=f, stderr=subprocess.STDOUT)

# Wait for URL
url_pattern = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
url = None
for i in range(20):
    time.sleep(2)
    try:
        content = open(TUNNEL_LOG).read()
        match = url_pattern.search(content)
        if match:
            url = match.group(0)
            break
    except: pass
    print(f"Waiting {i+1}/20", flush=True)

if not url:
    # Check log for errors
    log = open(TUNNEL_LOG).read()
    errors = [l for l in log.split("\n") if "error" in l.lower() or "fail" in l.lower() or "ERR" in l]
    print(f"Tunnel FAILED. Log last 20 lines:", flush=True)
    for l in log.split("\n")[-20:]:
        print(f"  {l}", flush=True)
    tunnel_proc.kill()
    flask_proc.kill()
    exit(1)

print(f"TUNNEL_URL={url}", flush=True)

# Test tunnel URL
time.sleep(3)
try:
    r = urllib.request.urlopen(url + "/api/domains", timeout=10)
    print(f"Tunnel test: OK ({r.status})", flush=True)
except Exception as e:
    print(f"Tunnel test: FAILED - {e}", flush=True)

# Check DNS
try:
    import socket
    hostname = url.split("://")[1].split("/")[0]
    ip = socket.gethostbyname(hostname)
    print(f"DNS resolve: {hostname} -> {ip}", flush=True)
except Exception as e:
    print(f"DNS resolve: FAILED - {e}", flush=True)

print("\nKeeping services alive for 120s for you to test...", flush=True)
time.sleep(120)

tunnel_proc.kill()
flask_proc.kill()
print("Stopped.", flush=True)
