import asyncio
import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# Environment variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
owner_id = int(os.environ.get("OWNER_ID"))

# Create client session
client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(pattern=r"/clean (.+)"))
async def clean_all(event):
    # Allow only owner to run command
    if event.sender_id != owner_id:
        return

    channel = event.pattern_match.group(1).strip()

    try:
        entity = await client.get_entity(channel)
    except Exception as e:
        await event.reply(f"❌ Invalid channel username\n\nError: {e}")
        return

    msg = await event.reply(f"🧹 Cleaning started for {channel}...\nPlease wait...")

    deleted = 0

    async for message in client.iter_messages(entity):
        try:
            await message.delete()
            deleted += 1

            # Update progress every 100 messages
            if deleted % 100 == 0:
                await msg.edit(f"🧹 Cleaning {channel}\nDeleted: {deleted}")

            await asyncio.sleep(0.5)

        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

        except Exception:
            pass

    await msg.edit(f"✅ Cleaning completed for {channel}\nTotal deleted: {deleted}")

# Start client
client.start()
client.run_until_disconnected()
