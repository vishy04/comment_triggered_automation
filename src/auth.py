import os
from instagrapi import Client

def login_instagram() -> Client:
    session_file = "session.json"
    
    if os.path.exists(session_file):
        client = Client()
        try:
            client.load_settings(session_file)
            client.get_timeline_feed()
            print("Session loaded from cache and verified.")
            return client
        except Exception as e:
            print(f"Cached session invalid or expired: {e}")
            print("Attempting fresh login...")


    client = Client()
    username = os.environ.get("IG_USERNAME")
    password = os.environ.get("IG_PASSWORD")
    if not username or not password:
        raise ValueError("Missing IG_USERNAME or IG_PASSWORD in .env")
        
    client.login(username, password)
    client.dump_settings(session_file)
    print("Login successful. Session saved.")
    return client
