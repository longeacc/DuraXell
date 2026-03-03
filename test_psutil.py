import sys
import psutil

print("Checking if we have dangling tracker processes...")
for p in psutil.process_iter(['name', 'cmdline']):
    cmd = " ".join(p.info.get('cmdline') or [])
    if "python" in p.info['name'] and "eco2ai" in cmd:
        print(f"Found running tracker {p.pid}")
