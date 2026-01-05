import os
import json
from datetime import datetime
from instagrapi import Client

class RateLimiter:
    def __init__(self, limit=30, state_file="data/rate_limit.json"):
        self.limit = limit
        self.state_file = state_file
        self.count = 0
        self.last_date = ""
        os.makedirs(os.path.dirname(state_file), exist_ok=True) if os.path.dirname(state_file) else None
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.count = data.get("count", 0)
                    self.last_date = data.get("last_date", "")
            except Exception:
                pass
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        if self.last_date != current_date:
            self.count = 0
            self.last_date = current_date
            self.save_state()

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump({"count": self.count, "last_date": self.last_date}, f)

    def increment(self):
        self.load_state()
        self.count += 1
        self.save_state()

    def is_limited(self) -> bool:
        self.load_state()
        return self.count >= self.limit

class DMSender:
    def __init__(self):
        try:
            limit = int(os.environ.get("DAILY_DM_LIMIT", 30))
        except ValueError:
            limit = 30
        self.limiter = RateLimiter(limit=limit)
        
    def send_dm(self, user_id: str, message: str, client: Client = None) -> str:
        if self.limiter.is_limited():
            print(f"Daily DM limit ({self.limiter.limit}) reached. Delaying operation.")
            return "limit_reached"
            
        if os.environ.get("DRY_RUN", "").lower() == "true":
            print(f"Dry run: Would DM {user_id} -> {message}")
            self.limiter.increment()
            return "dry_run"
            
        try:
            if client:
                client.direct_send(message, user_ids=[int(user_id)])
            print(f"Sent DM to {user_id}")
            self.limiter.increment()
            return "sent"
        except Exception as e:
            print(f"Failed to DM {user_id}: {e}")
            return "failed"
