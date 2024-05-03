
# The main file for PzPy bot. Sets up and runs the discord client
from modules.chat import ChatHandler
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from modules.maps import MapHandler
import os
from pathlib import Path
from modules.perks import PerkHandler
from modules.users import UserHandler
from modules.admin import AdminLogHandler
from modules.rcon_adapter import RCONAdapter
import modules.embed
import gettext
load_dotenv(override=True)

#setup gettext
appname = 'zomboid_bot'
localedir = os.getenv("LANGUAGE_DIR")
language= os.getenv("BOT_LANGUAGE")
bot_translate = gettext.translation(appname, localedir, fallback=False, languages=[language])
bot_translate.install(names=['ngettext'])



# Verify the log path
logPath = os.getenv("LOGS_PATH")
if logPath is None or len(logPath) == 0:
    path = Path.home().joinpath("Zomboid/Logs")
    if path.exists():
        logPath = str(path)
    else:
        logging.error("Zomboid log path not set and/or unable to find default")
        exit()
        
# Verify the users data directory path
dataPath = os.getenv("DATA_PATH")
if dataPath is None or len(dataPath) == 0:
    path = Path.cwd().joinpath("data")
    if path.exists():
        dataPath = str(path)
    else:
        logging.error("Users data path not set and/or unable to find default")
        exit()        

# Our main bot object
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
PzPy = commands.bot.Bot("!", intents=intents)

# Redirect the discord log to a file
logFormat = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
discordLogger = logging.getLogger("discord")
discordLogger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logFormat)
discordLogger.addHandler(handler)

# set up our logging
PzPy.log = logging.getLogger("PzPy")
handler = logging.StreamHandler()
handler.setFormatter(logFormat)
handler.setLevel(logging.INFO)
PzPy.log.addHandler(handler)
handler = logging.FileHandler(filename="logs/PzPy.log")
handler.setFormatter(logFormat)
handler.setLevel(logging.DEBUG)
PzPy.log.addHandler(handler)
PzPy.log.setLevel(logging.DEBUG)


@PzPy.event
async def on_ready():
    PzPy.log.info(f"We have logged in as {PzPy.user}")
    channel = os.getenv("CHANNEL")
    PzPy.channel = (  # Find by id
        PzPy.get_channel(int(channel)) if channel.isdigit() else None
    )
    if PzPy.channel is None:
        PzPy.channel = discord.utils.get(
            PzPy.get_all_channels(), name=channel
        )  # find by name
    if PzPy.channel is None:
        PzPy.log.warning("Unable to get channel, will not be enabled")
    else:
        PzPy.log.info("channel connected")
    await PzPy.add_cog(UserHandler(PzPy, logPath, dataPath))
    await PzPy.add_cog(ChatHandler(PzPy, logPath))
    await PzPy.add_cog(PerkHandler(PzPy, logPath, dataPath))
    await PzPy.add_cog(RCONAdapter(PzPy))
    await PzPy.add_cog(MapHandler(PzPy))
    await PzPy.add_cog(AdminLogHandler(PzPy, logPath))


# Always finally run the bot
token = os.getenv("DISCORD_TOKEN")
if token is None:
    PzPy.log.error("DISCORD_TOKEN environment variable not found")
    exit()

PzPy.run(os.getenv("DISCORD_TOKEN"))
