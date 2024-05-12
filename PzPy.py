from pathlib import Path
import os
import logging
import coloredlogs, logging
# Verify if configuratin exist
path = Path.cwd().joinpath(".env")
isFile = os.path.isfile(path)
if not isFile:
    logging.error("PzPy.py : ERROR : Unable to find the configuration file (.env). Edit sample.env and rename it to .env.")
    exit()
 
# The main file for PzPy bot. Sets up and runs the discord client
import discord
from discord.ext import commands
from dotenv import load_dotenv
import gettext
from modules.checkConfig import checkConfigDiscord, checkConfig
from modules.perkReader import perkReader
from modules.userReader import userReader
from modules.consoleReader import consoleReader
from modules.chatReader import chatReader
from modules.modUpdater import modUpdater
from modules.admin import AdminLogHandler
from modules.rcon_adapter import RCONAdapter
import modules.embed
import asyncio
load_dotenv(override=True)


#setup gettext
appname = 'zomboid_bot'
localedir = os.getenv("LANGUAGE_DIR")
language= os.getenv("BOT_LANGUAGE")
bot_translate = gettext.translation(appname, localedir, fallback=False, languages=[language])
bot_translate.install(names=['ngettext'])

#Check the configuration (.env) file data
asyncio.run(modules.checkConfig.checkConfig.run())

# Init logPath
logPath = os.getenv("LOGS_PATH")
if logPath is None or len(logPath) == 0:
    path = Path.home().joinpath("Zomboid/Logs")
    if path.exists():
        logPath = str(path)
        
# Init dataPath
dataPath = os.getenv("DATA_PATH")
if dataPath is None or len(dataPath) == 0:
    path = Path.cwd().joinpath("data")
    if path.exists():
        dataPath = str(path)     

# Our main bot object
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
PzPy = commands.bot.Bot("!", intents=intents)

# Redirect the discord log to a file
logFormat = logging.Formatter(os.getenv("COLOREDLOGS_LOG_FORMAT"))
discordLogger = logging.getLogger("discord")
discordHandler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8", mode="w")
discordHandler.setFormatter(logFormat)
discordLogger.addHandler(discordHandler)

# set up our logging
PzPy.log = logging.getLogger("PzPy")
coloredlogs.install(level=os.getenv("LOG_LEVEL"), logger=PzPy.log)
PzPyHandler = logging.FileHandler(filename="logs/PzPy.log")
PzPy.log.addHandler(PzPyHandler)

   
@PzPy.event
async def on_ready():
    PzPy.log.info(f"PzPy.py : We have logged in as {PzPy.user}")
    channel = os.getenv("CHANNEL")
    PzPy.channel = (  # Find by id
        PzPy.get_channel(int(channel)) if channel.isdigit() else None
    )
    if PzPy.channel is None:
        PzPy.channel = discord.utils.get(
            PzPy.get_all_channels(), name=channel
        )  # find by name
    if PzPy.channel is None:
        PzPy.log.warning("PzPy.py : ERROR : Unable to get channel, will not be enabled")
    else:
        PzPy.log.info("PzPy.py : channel connected")

    await PzPy.add_cog(checkConfigDiscord(PzPy))
    await PzPy.add_cog(userReader(PzPy, logPath, dataPath))
    await PzPy.add_cog(chatReader(PzPy, logPath))
    await PzPy.add_cog(perkReader(PzPy, logPath, dataPath))
    await PzPy.add_cog(RCONAdapter(PzPy))
    await PzPy.add_cog(modUpdater(PzPy))
    await PzPy.add_cog(AdminLogHandler(PzPy, logPath))
    await PzPy.add_cog(consoleReader(PzPy, logPath, dataPath))


# Always finally run the bot
token = os.getenv("DISCORD_TOKEN")
if token is None:
    PzPy.log.error("PzPy.py : ERROR : DISCORD_TOKEN environment variable not found")
    exit()

PzPy.run(os.getenv("DISCORD_TOKEN"))
