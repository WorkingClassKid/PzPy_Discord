from datetime import datetime
import discord
from discord.ext import tasks, commands
from discord import Embed, Colour
from file_read_backwards import FileReadBackwards
import glob
import os
import re
import hashlib
import modules.embed
import modules.usersData
import modules.serverData
import modules.modUpdater


# Class which handles and read the console.log file
class consoleReader(commands.Cog):
    def __init__(self, bot, logPath, dataPath):
        self.bot = bot
        self.logPath = logPath
        self.dataPath = dataPath
        self.lastMessageHash = None
        self.lastUpdateRealTimestamp = datetime.timestamp(datetime.now())*1000
        self.sendLogs = True
        # If the user has not enabled Admin logs, let's exit
        if not self.sendLogs:
            return
        self.adminChannel = os.getenv("ADMIN_CHANNEL")
        if not self.adminChannel:
            self.bot.log.warning(
                "Unable to get admin channel, setting to default channel..."
            )
            self.adminChannel = self.bot.channel.name
        if self.adminChannel.isdigit():
            self.adminChannel = self.bot.get_channel(
                int(self.adminChannel)
            )  # Find by id
        if isinstance(self.adminChannel, str):
            self.adminChannel = discord.utils.get(
                self.bot.get_all_channels(), name=self.adminChannel
            )  # find by name        
        self.update.start()


    def splitLine(self, line: str) -> tuple[datetime, str]:
        """Split a log line into a timestamp and the remaining message"""
        timestampStr, trash, message = line.strip()[1:].split(">", 2)
        # Ignore the start of the message before the timestamp
        timestampStr = timestampStr[timestampStr.find(",", 2) + 1 :]
        timestampStr = timestampStr.translate({ord(' '): None}) #fix unknown space issue
        return timestampStr, message
    
    @tasks.loop(seconds=2)
    async def update(self) -> None:
        files = glob.glob(os.getenv("PZ_PATH") + "/server-console.txt")
        if len(files) > 0:
            with FileReadBackwards(files[0], encoding="utf-8") as f:
                for line in f:
                    if "LOG" in line :
                        messageTimestamp, message = self.splitLine(line)
                        messageTimestamp = int(messageTimestamp)
                        if messageTimestamp >= self.lastUpdateRealTimestamp:
                            messageHash = hashlib.md5(line.encode('utf-8')).hexdigest() 
                            if self.lastMessageHash != messageHash:
                                embed = await self.readLog(messageTimestamp, message, fromUpdate=True)
                                self.lastMessageHash = messageHash
                                if embed is not None and self.bot.channel is not None:
                                    await self.bot.channel.send(embed=embed)
                        else:
                            self.lastUpdateRealTimestamp = datetime.timestamp(datetime.now())*1000                   
                            break
                        


    # Parse a line in the server-console.txt file and take appropriate action

    async def readLog(self, timestamp: datetime, message: str, fromUpdate=False) -> Embed | None:
    
        if "EHE: LAUNCH:" in message :
            self.bot.log.info(f"consoleReader.py : EHE EVENT : CHOOOOOPPAAAAA")
        
        elif "CheckModsNeedUpdate: Mods updated" in message :
            self.bot.log.info(f"consoleReader.py : CheckModsNeedUpdate : All mods are up-to-date")
            await self.adminChannel.send(f"PzPy : consoleReader.py : CheckModsNeedUpdate : All mods are up-to-date")
            
        elif "CheckModsNeedUpdate: Mods need update" in message :
            self.bot.log.warning(f"consoleReader.py : CheckModsNeedUpdate : One or more mod(s) need to be updated.")
            await self.adminChannel.send(f"PzPy : consoleReader.py : CheckModsNeedUpdate : One or more mod(s) need to be updated.")
            await modules.modUpdater.modUpdater.startUpdate(self)
        else:
            self.bot.log.debug(f"consoleReader.py : Ignored : {message}")
   
 

