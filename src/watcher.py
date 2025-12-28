import os

def load_seen(file_path="seen.txt"):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r") as f:
        return set(f.read().splitlines())

def mark_seen(comment_id, file_path="seen.txt"):
    with open(file_path, "a") as f:
        f.write(f"{comment_id}\n")

def poll_comments(client, media_id, keyword, seen_set):
    matches = []
    try:
        # Only fetch latest 50 comments to avoid hitting aggressive API limits with amount=0
        comments = client.media_comments(media_id, amount=50)
        for comment in comments:
            if keyword.lower() in comment.text.lower() and str(comment.pk) not in seen_set:
                matches.append(comment)
    except Exception as e:
        print(f"Error checking comments: {e}")
    return matches
