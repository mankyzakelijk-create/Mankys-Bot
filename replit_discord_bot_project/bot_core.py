# bot_core.py
import discord
from discord.ext import commands
import os
import json

CMD_FILE = os.path.join(os.path.dirname(__file__), 'commands.json')

intents = discord.Intents.all()
PREFIX = os.getenv('PREFIX', '!')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def load_commands():
    if not os.path.exists(CMD_FILE):
        with open(CMD_FILE, 'w') as f:
            json.dump({}, f)
    with open(CMD_FILE, 'r') as f:
        return json.load(f)

@bot.event
async def on_ready():
    print(f'Bot is ready als: {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # eenvoudige custom commands (exact match zonder prefix)
    if message.content.startswith(PREFIX):
        cmd = message.content[len(PREFIX):].strip().split(' ')[0]
        cmds = load_commands()
        if cmd in cmds:
            await message.channel.send(cmds[cmd])
            return
    await bot.process_commands(message)

def run_bot():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print('ERROR: Zet DISCORD_TOKEN in Replit Secrets')
        return
    bot.run(token)
