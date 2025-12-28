import os
from instagrapi import Client

class DMSender:
    def send_dm(self, user_id: str, message: str, client: Client = None) -> str:
        if os.environ.get("DRY_RUN", "").lower() == "true":
            print(f"Dry run: Would DM {user_id} -> {message}")
            return "dry_run"
            
        try:
            if client:
                client.direct_send(message, user_ids=[int(user_id)])
            print(f"Sent DM to {user_id}")
            return "sent"
        except Exception as e:
            print(f"Failed to DM {user_id}: {e}")
            return "failed"
