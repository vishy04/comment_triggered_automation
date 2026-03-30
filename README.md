# Instagram Comment-Triggered DM Bot

A lightweight, automated Python script that monitors multiple Instagram posts/reels simultaneously for specific keywords in the comments and safely sends a direct message (DM) to the commenter.

## Features

- **Multi-Reel Monitoring**: Watches an array of posts, each with its own designated keyword and custom message.
- **SQLite Deduplication**: Uses a robust SQLite database to ensure the bot never messages the same user twice.
- **Anti-Bot Guardrails**: Designed with `instagrapi` evasion techniques:
  - Spoofs consistent Android hardware.
  - Implements massive 5-15 minute randomized sleep logic between DMs.
  - Supports proxies and enforces safe maximum daily limits.
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
   REELS_CONFIG='[{"media_id": "1234567890", "keyword": "LINK", "message": "Here is your link!"}]'
   DAILY_DM_LIMIT=30
   IG_PROXY=
   POLL_INTERVAL=60
   DRY_RUN=true
   ```

   *Helper:* If you don't know your `media_id`, simply run the included tool to extract it from any post URL:

   ```bash
   python src/get_media_id.py "https://www.instagram.com/p/XXXXXXX/"
   ```

## Usage

Start the bot by running:

```bash
uv run python src/main.py
```

> **Tip**: Always leave `DRY_RUN=true` during your initial testing to ensure the bot is successfully matching the keyword. Change it to `false` when you're ready to start sending actual messages!
