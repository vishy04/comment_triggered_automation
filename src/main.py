import os
import sys
import time
import json
import random
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import login_instagram
from src.watcher import load_seen, mark_seen, poll_comments
from src.sender import DMSender
from src.llm_responder import generate_dm_response

def main():
    load_dotenv()
    
    reels_config_str = os.getenv("REELS_CONFIG")
    
    if not reels_config_str:
        print("Missing REELS_CONFIG in .env")
        sys.exit(1)

    try:
        reels_config = json.loads(reels_config_str)
    except json.JSONDecodeError:
        print("Error: REELS_CONFIG is not a valid JSON string.")
        sys.exit(1)

    print("Authenticating...")
    client = login_instagram()
    sender = DMSender()
    seen = load_seen()
    
    print(f"Monitoring {len(reels_config)} reel(s). Press Ctrl+C to stop.")
    
    while True:
        try:
            for config in reels_config:
                media_id = config.get("media_id")
                keyword = config.get("keyword")
                message = config.get("message")
                
                if not all([media_id, keyword, message]):
                    print(f"Skipping malformed config payload: {config}")
                    continue

                matches = poll_comments(client, media_id, keyword, seen)
                for comment in matches:
                    print(f"Match found by {comment.user.pk} on {media_id}")
                    
                    # Generate LLM response, falling back to static message config if failed
                    dynamic_message = generate_dm_response(comment.text, fallback_message=message)
                    
                    status = sender.send_dm(str(comment.user.pk), dynamic_message, client)
                    
                    if status == "limit_reached":
                        print("Daily limit reached. Pausing DMs and sleeping for 1 hour before rechecking...")
                        time.sleep(3600)
                        break # Break the matches loop, will sleep again next cycle if still limited

                    if status in ["sent", "dry_run"]:
                        mark_seen(comment.pk)
                        seen.add(str(comment.pk))
                    
                    # Massive 5-15 minute wait between DM dispatching
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
