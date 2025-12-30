import os
import sys
import time
import random
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import login_instagram
from src.watcher import load_seen, mark_seen, poll_comments
from src.sender import DMSender

def main():
    load_dotenv()
    
    media_id = os.getenv("MEDIA_ID")
    keyword = os.getenv("KEYWORD")
    dm_message = os.getenv("DM_MESSAGE")
    
    if not all([media_id, keyword, dm_message]):
        print("Missing .env configuration variables.")
        sys.exit(1)

    print("Authenticating...")
    client = login_instagram()
    sender = DMSender()
    seen = load_seen()
    
    print(f"Polling {media_id} for '{keyword}'... (Ctrl+C to stop)")
    
    while True:
        try:
            matches = poll_comments(client, media_id, keyword, seen)
            for comment in matches:
                print(f"Match found by {comment.user.pk}")
                status = sender.send_dm(str(comment.user.pk), dm_message, client)
                if status in ["sent", "dry_run"]:
                    mark_seen(comment.pk)
                    seen.add(str(comment.pk))
                time.sleep(2)  # small pause between DMs
                
            time.sleep(random.randint(45,75)) # jittered poll wait
        except KeyboardInterrupt:
            print("\nStopping bot gracefully...")
            break

if __name__ == "__main__":
    main()
