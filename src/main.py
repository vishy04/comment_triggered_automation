import os
import sys
import time
import json
import random
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import login_instagram
from src.watcher import load_seen, mark_seen, poll_global_comments, fetch_recent_reels
from src.sender import DMSender
from src.llm_responder import generate_dm_response

def main():
    load_dotenv()
    
    campaigns_str = os.getenv("GLOBAL_CAMPAIGNS")
    
    if not campaigns_str:
        print("Missing GLOBAL_CAMPAIGNS in .env")
        sys.exit(1)

    try:
        campaigns = json.loads(campaigns_str)
    except json.JSONDecodeError:
        print("Error: GLOBAL_CAMPAIGNS is not a valid JSON dict.")
        sys.exit(1)

    print("Authenticating...")
    client = login_instagram()
    sender = DMSender()
    seen = load_seen()
    
    last_fetch_time = 0
    recent_reels = []
    
    print(f"Monitoring Campaigns globally mapping to: {list(campaigns.keys())}. Press Ctrl+C to stop.")
    
    while True:
        try:
            current_time = time.time()
            
            # Fetch reel cache dynamically every 12 hours (43200 seconds) securely preventing ban spikes
            if current_time - last_fetch_time > 43200:
                print("Fetching reels posted within the last 7 days...")
                recent_reels = fetch_recent_reels(client, days=7)
                last_fetch_time = current_time
                print(f"Tracking {len(recent_reels)} dynamic reel(s).")
                
            if not recent_reels:
                print("No recent reels found in 7-day window. Sleeping sequence...")
                time.sleep(3600)
                continue

            for media_id in recent_reels:
                matches = poll_global_comments(client, media_id, campaigns, seen)
                
                for comment, target_message in matches:
                    print(f"Campaign Context Matched by {comment.user.pk} on {media_id}")
                    
                    dynamic_message = generate_dm_response(comment.text, fallback_message=target_message)
                    
                    status = sender.send_dm(str(comment.user.pk), dynamic_message, client)
                    
                    if status == "limit_reached":
                        print("Daily limit reached. Pausing DMs and sleeping for 1 hour before rechecking...")
                        time.sleep(3600)
                        break 

                    if status in ["sent", "dry_run"]:
                        mark_seen(comment.pk)
                        seen.add(str(comment.pk))
                    
                    delay = random.randint(300, 900)
                    print(f"Staggering next DM dispatch. Sleeping for {delay} seconds...")
                    time.sleep(delay)
                    
            poll_interval = int(os.environ.get("POLL_INTERVAL", "60"))
            time.sleep(poll_interval)
            
        except KeyboardInterrupt:
            print("\nStopping bot gracefully...")
            break

if __name__ == "__main__":
    main()
