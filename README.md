# KomootGPX Telegram Bot

Telegram bot for downloading Komoot routes as GPX files by link. Works only with public routes, caches downloaded files, and limits each user to 30 downloads per hour.

**This bot uses [KomootGPX](https://github.com/timschneeb/KomootGPX) for downloading GPX files from Komoot.**

## Features
- Accepts Komoot route links
- Extracts route id
- Downloads GPX file via komootgpx
- Caches files
- Generates a safe file name before sending
- Limit: 30 downloads per hour per user

## Quick Start

### 1. Clone the repository and go to the folder
```bash
git clone <repo_url>
cd gpx_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install komootgpx
```bash
pip install komootgpx
```

### 4. Run the bot
```bash
TELEGRAM_TOKEN=your_token_here python bot.py
```

## Environment variables
- `TELEGRAM_TOKEN` — Telegram bot token (required)

## Docker

### Build and run
```bash
docker build -t komootgpx-bot .
docker run -e TELEGRAM_TOKEN=your_token_here -v $(pwd)/cache:/app/cache komootgpx-bot
```

## Docker Compose

Example `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      - TELEGRAM_TOKEN=your_token_here
    volumes:
      - ./cache:/app/cache
```

Run:
```bash
docker-compose up --build
```

## Usage example
1. Send the bot a Komoot route link (e.g., https://www.komoot.com/tour/123456789)
2. Receive the GPX file in response

## License
MIT

---

*This project was fully written with the help of AI.* 