import time
import os
import requests
from datetime import datetime
from picamera2 import Picamera2

# === Configurations ===
SERVER_URL = "http://45.154.24.169:8000/upload/RaspberryPi1"
PHOTO_DIR = os.path.expanduser("~/photos")
INTERVAL = 30  # seconds between uploads

# === Ensure photo directory exists ===
os.makedirs(PHOTO_DIR, exist_ok=True)

# === Initialize the camera ===
try:
    camera = Picamera2()
    camera.start()
    print("[🎥] Camera initialized.")
except Exception as e:
    print(f"[❌] Failed to initialize camera: {e}")
    exit(1)

def capture_and_send():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)

    try:
        # Capture photo
        camera.capture_file(filepath)
        print(f"[📸] Captured: {filepath}")
    except Exception as e:
        print(f"[❌] Failed to capture image: {e}")
        return

    try:
        # Upload photo to server
        with open(filepath, "rb") as f:
            files = {"file": (filename, f, "image/jpeg")}
            response = requests.post(SERVER_URL, files=files, timeout=10)
        
        if response.status_code == 200:
            print(f"[✅] Uploaded successfully: {filename}")
        else:
            print(f"[⚠️] Upload failed ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[🚫] Network error: {e}")
    except Exception as e:
        print(f"[❌] Unexpected error during upload: {e}")

def main():
    print("[🔁] Starting capture/upload loop...")
    while True:
        capture_and_send()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
