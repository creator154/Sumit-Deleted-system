import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
owner_id = int(os.environ["OWNER_ID"])
string_session = os.environ["STRING_SESSION"]

client = TelegramClient(StringSession(string_session), api_id, api_hash)

@client.on(events.NewMessage(pattern=r"/clean (.+)"))
async def clean_all(event):
    if event.sender_id != owner_id:
        return

    channel = event.pattern_match.group(1).strip()
    entity = await client.get_entity(channel)

    msg = await event.reply("Cleaning started...")
    deleted = 0

    async for message in client.iter_messages(entity):
        try:
            await message.delete()
            deleted += 1
            await asyncio.sleep(0.5)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

    await msg.edit(f"Done ✅ Deleted: {deleted}")

client.start()
client.run_until_disconnected()
