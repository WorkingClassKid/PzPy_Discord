import os
from pathlib import Path
import discord
from discord.ext import tasks, commands
from rcon.source import Client, rcon


class checkConfigDiscord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
        # Test if ADMIN_CHANNEL is valid
        # Test if ADMIN_CHANNEL is valid
        if not os.getenv("ADMIN_CHANNEL"):
            self.bot.log.error("checkConfig.py : Unable to get ADMIN_CHANNEL. Check your configuration file")
            exit("checkConfig.py : Unable to get ADMIN_CHANNEL, check your configuration file")
            
        if os.getenv("ADMIN_CHANNEL").isdigit():
            adminChannel = self.bot.get_channel(
                int(os.getenv("ADMIN_CHANNEL"))
            )
        else:
            if isinstance(os.getenv("ADMIN_CHANNEL"), str):
                adminChannel = discord.utils.get(
                    self.bot.get_all_channels(), name=os.getenv("ADMIN_CHANNEL")
                )  # find by name 
        if adminChannel is None:
            self.bot.log.error("checkConfig.py : Invalid ADMIN_CHANNEL, check your configuration file")
            exit("checkConfig.py : Invalid ADMIN_CHANNEL, check your configuration file")   
            
   
   
class checkConfig(): 
   
    # Check for rcon configuration
    async def checkConfigRcon():
        try:
            response = await rcon(
                "checkModsNeedUpdate",
                host=os.getenv("RCON_HOST"),
                port=os.getenv("RCON_PORT"),
                passwd=os.getenv("RCON_PASSWORD"),
            )    
        except:
            exit("checkConfig.py : Invalid rcon configuration. Check your configuration file (RCON_HOST, RCON_PORT and RCON_PASSWORD)")
    
    # Verify the log path
    async def checkConfigLogPath(logPath):
        if logPath is None or len(logPath) == 0:
            path = Path.home().joinpath("Zomboid/Logs")
            if path.exists():
                logPath = str(path)
        else:
            logPath = Path(logPath)
            if logPath.exists():
                logPath = str(logPath)
            else :    
                exit("PzPy.py : ERROR : Zomboid log path not set and/or unable to find default. Check your configuration file (LOGS_PATH)")



    async def run():
        await checkConfig.checkConfigRcon()
        await checkConfig.checkConfigLogPath(os.getenv("LOGS_PATH"))

    
    