
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch

API_ID = int(os.getenv("34703550"))
API_HASH = os.getenv("624c1a91b4b2bdd8186f4a988cd00b49")
BOT_TOKEN = os.getenv("8202480716:AAHa6DjAU2BAgQqjGffVAra8E7s0xcFd3_A")

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

@app.on_message(filters.command("play") & filters.group)
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /play song name")

    query = " ".join(message.command[1:])
    msg = await message.reply(f"Searching **{query}** ...")

    search = VideosSearch(query, limit=1).result()
    if not search["result"]:
        return await msg.edit("No results found.")

    url = search["result"][0]["link"]
    title = search["result"][0]["title"]

    await msg.edit(f"Downloading **{title}** ...")
    os.system(f'yt-dlp -q -o "song.mp3" -x --audio-format mp3 {url}')

    chat_id = message.chat.id
    await call.join_group_call(
        chat_id,
        InputStream(
            AudioPiped("song.mp3")
        ),
        stream_type=StreamType().local_stream,
    )

    await msg.edit(f"🎶 Now playing: **{title}**")

@app.on_message(filters.command("stop") & filters.group)
async def stop_handler(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("⏹ Stopped playback.")
    except:
        await message.reply("Bot is not playing anything.")

call.start()
app.start()
idle()
