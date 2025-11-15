import discord
from discord.ext import commands
import json
import os
from gui import start_gui

TOKEN = os.getenv("DISCORD_TOKEN")  # Zet in Replit secrets!

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def load_commands():
    with open("commands.json", "r") as f:
        return json.load(f)

@bot.event
async def on_ready():
    print(f"Bot is online als {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    cmds = load_commands()
    msg = message.content.lower().strip()

    if msg.startswith("!"):
        cmd = msg[1:]
        if cmd in cmds:
            await message.channel.send(cmds[cmd])
    
    await bot.process_commands(message)

# Start GUI server in background
start_gui()

bot.run(TOKEN)
