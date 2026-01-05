import os
from instagrapi import Client

def login_instagram() -> Client:
    session_file = "session.json"
    proxy = os.environ.get("IG_PROXY")
    
    if os.path.exists(session_file):
        client = Client()
        if proxy:
            client.set_proxy(proxy)
        try:
            client.load_settings(session_file)
            client.get_timeline_feed()
            print("Session loaded from cache and verified.")
            return client
        except Exception as e:
            print(f"Cached session invalid or expired: {e}")
            print("Attempting fresh login...")

    client = Client()
    if proxy:
        client.set_proxy(proxy)
        
    device_settings = {
        "app_version": "269.0.0.18.75",
        "android_version": "33",
        "android_release": "13",
        "dpi": "480dpi",
        "resolution": "1080x2400",
        "manufacturer": "samsung",
        "device": "SM-G991U",
        "model": "q2q",
        "cpu": "qcom",
        "version_code": "314665256"
    }
    client.set_device(device_settings)
    
    username = os.environ.get("IG_USERNAME")
    password = os.environ.get("IG_PASSWORD")
    if not username or not password:
        raise ValueError("Missing IG_USERNAME or IG_PASSWORD in .env")
        
    client.login(username, password)
    client.dump_settings(session_file)
    print("Login successful. Session saved.")
    return client
