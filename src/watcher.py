import os
import sqlite3

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

def poll_comments(client, media_id, keyword, seen_set):
    matches = []
    try:
        comments = client.media_comments(media_id, amount=50)
        for comment in comments:
            if keyword.lower() in comment.text.lower() and str(comment.pk) not in seen_set:
                matches.append(comment)
    except Exception as e:
        print(f"Error checking comments on {media_id}: {e}")
    return matches
