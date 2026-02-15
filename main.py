import asyncio
import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH"))
owner_id = int(os.environ.get("OWNER_ID"))

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(pattern=r"/clean (.+)"))
async def clean_all(event):
    if event.sender_id != owner_id:
        return

    channel = event.pattern_match.group(1)
    msg = await event.reply(f"Cleaning started for {channel}...")

    deleted = 0

    async for message in client.iter_messages(channel):
        try:
            await message.delete()
            deleted += 1
            
            if deleted % 100 == 0:
                await msg.edit(f"Deleted {deleted} messages...")
            
            await asyncio.sleep(0.4)

        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

    await msg.edit(f"✅ Cleaning completed\nTotal deleted: {deleted}")

client.start()
client.run_until_disconnected()
