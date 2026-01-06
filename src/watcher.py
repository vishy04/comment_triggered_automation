import os
import sqlite3
from datetime import datetime, timedelta

_db_path = "data/seen.db"

def init_db(db_path=_db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS seen_comments (
            comment_id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def load_seen(db_path=_db_path):
    init_db(db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.execute("SELECT comment_id FROM seen_comments")
    seen = set(row[0] for row in cursor.fetchall())
    conn.close()
    return seen

def mark_seen(comment_id, db_path=_db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    try:
        conn.execute("INSERT INTO seen_comments (comment_id) VALUES (?)", (str(comment_id),))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def fetch_recent_reels(client, days=7):
    recent_medias = []
    try:
        user_id = client.user_id
        # amount=20 is sufficient buffer to scrape a highly active user's past 7 days
        medias = client.user_medias(user_id, amount=20)
        
        # media.taken_at natively yields offset-aware datetimes
        # so we extract the plain naive datetime to compare generically
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for media in medias:
            # strip timezone info to safely equate
            taken_at_naive = media.taken_at.replace(tzinfo=None)
            if taken_at_naive >= cutoff_date:
                recent_medias.append(media.pk)
    except Exception as e:
        print(f"Error fetching recent reels: {e}")
    return recent_medias

def poll_global_comments(client, media_id, campaigns, seen_set):
    matches = []
    try:
        comments = client.media_comments(media_id, amount=50)
        for comment in comments:
            if str(comment.pk) in seen_set:
                continue
                
            normalized_text = comment.text.lower().strip()
            
            # Loop against the provided global dictionary mapping keywords seamlessly
            for keyword, target_message in campaigns.items():
                normalized_keyword = str(keyword).lower().strip()
                if normalized_keyword in normalized_text:
                    matches.append((comment, target_message))
                    break
    except Exception as e:
        print(f"Error checking comments on {media_id}: {e}")
    return matches
