# Instagram Comment-Triggered DM Bot

A lightweight, automated Python script that monitors an Instagram post or reel for a specific keyword in the comments and instantly sends a direct message (DM) to the commenter. 

## Features
- **Real-time Polling**: Continuously watches a specific post for new comments.
- **Smart Deduplication**: Never messages the same user twice.
- **Auto-Authentication**: Caches your Instagram session to prevent repeated logins and avoid rate-limits.
- **Safe Dry-Run Mode**: Test your configuration without actually sending DMs.

## Setup & Configuration

1. **Install dependencies** (using `uv` or `pip`):
   ```bash
   uv sync
   ```

2. **Configure Environment:**
   Rename `.env.example` to `.env` and fill in your details:
   ```env
   IG_USERNAME=your_username
   IG_PASSWORD=your_password
   MEDIA_ID=post_media_id
   KEYWORD=LINK
   DM_MESSAGE=Here is your free resource: https://example.com
   DRY_RUN=true
   ```

   *Helper:* If you don't know your `MEDIA_ID`, simply run the included tool to extract it from any post URL:
   ```bash
   python src/get_media_id.py "https://www.instagram.com/p/XXXXXXX/"
   ```

## Usage

Start the bot by running:
```bash
uv run python src/main.py
```

> **Tip**: Always leave `DRY_RUN=true` during your initial testing to ensure the bot is successfully matching the keyword. Change it to `false` when you're ready to start sending actual messages!
