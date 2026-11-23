"""
Zero-dependency infrastructure health check using Python standard library.
Checks:
- Qdrant HTTP health endpoint (port 6333)
- Redis TCP ping/pong (port 6381)
- MongoDB TCP socket connectivity (port 27018)
"""

import socket
import urllib.request
import json
import sys

def check_qdrant(host="localhost", port=6333):
    url = f"http://{host}:{port}/readyz"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="ignore")
            if status == 200:
                print(f"[✓] Qdrant is healthy on http://{host}:{port} (Response: {body.strip()})")
                print(f"    -> Web Dashboard: http://{host}:{port}/dashboard")
                return True
    except Exception as e:
        print(f"[✗] Qdrant check failed: {e}")
        return False

def check_redis(host="localhost", port=6381):
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(b"PING\r\n")
            response = s.recv(1024)
            if b"+PONG" in response:
                print(f"[✓] Redis is healthy on {host}:{port} (PING -> PONG)")
                return True
            else:
                print(f"[!] Redis responded unexpectedly: {response}")
                return False
    except Exception as e:
        print(f"[✗] Redis check failed: {e}")
        return False

def check_mongodb(host="localhost", port=27018):
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            print(f"[✓] MongoDB port is open and accepting TCP connections on {host}:{port}")
            return True
    except Exception as e:
        print(f"[✗] MongoDB check failed: {e}")
        return False

def main():
    print("=" * 55)
    print("Running Infrastructure Health Checks...")
    print("=" * 55)
    qdrant_ok = check_qdrant()
    redis_ok = check_redis()
    mongo_ok = check_mongodb()
    print("=" * 55)

    if qdrant_ok and redis_ok and mongo_ok:
        print("ALL SERVICES ARE HEALTHY AND READY!")
        sys.exit(0)
    else:
        print("Some services failed the health check.")
        sys.exit(1)

if __name__ == "__main__":
    main()
