import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess
import time
from collections import defaultdict, deque
import glob
from slugify import slugify
import shutil

# Directory for cache
CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

# Regex to extract tour_id from Komoot link
tour_id_pattern = re.compile(r'komoot\.[^/]+/tour/(\d+)')

# Your Telegram bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')

# Limits: max 30 downloads per user per hour
DOWNLOAD_LIMIT = 30
LIMIT_WINDOW = 3600  # seconds
user_limits = defaultdict(lambda: deque(maxlen=DOWNLOAD_LIMIT))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me a Komoot route link and I will send you the GPX file.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = time.time()
    # Remove old timestamps
    while user_limits[user_id] and now - user_limits[user_id][0] > LIMIT_WINDOW:
        user_limits[user_id].popleft()
    if len(user_limits[user_id]) >= DOWNLOAD_LIMIT:
        await update.message.reply_text('You have exceeded the limit: no more than 30 downloads per hour. Please try again later.')
        return
    text = update.message.text.strip()
    match = tour_id_pattern.search(text)
    if not match:
        await update.message.reply_text('Please send a valid Komoot route link.')
        return
    tour_id = match.group(1)
    # Search for file by mask *-<id>.gpx
    gpx_files = glob.glob(f"{CACHE_DIR}/*-{tour_id}.gpx")
    if not gpx_files:
        # Download GPX via komootgpx (without -I, use original name)
        try:
            subprocess.run([
                'komootgpx',
                '-d', tour_id,
                '-o', CACHE_DIR,
                '-e',  # no POI
                '-n'   # anonymous mode
            ], check=True)
        except Exception as e:
            await update.message.reply_text(f'Error downloading GPX: {e}')
            return
        gpx_files = glob.glob(f"{CACHE_DIR}/*-{tour_id}.gpx")
        if not gpx_files:
            await update.message.reply_text('GPX file not found after download.')
            return
    orig_gpx = gpx_files[0]
    # Generate a safe file name for sending
    orig_name = os.path.basename(orig_gpx)
    base_part = orig_name.rsplit(f'-{tour_id}.gpx', 1)[0]
    safe_name = slugify(base_part)[:30] + f'-{tour_id}.gpx'
    temp_path = os.path.join(CACHE_DIR, safe_name)
    shutil.copyfile(orig_gpx, temp_path)
    # Record the download
    user_limits[user_id].append(now)
    # Send file to user
    with open(temp_path, 'rb') as f:
        await update.message.reply_document(f, filename=safe_name)
    os.remove(temp_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print('Bot started...')
    app.run_polling() 