from datetime import datetime
from discord import Embed
from discord.ext import tasks, commands
from file_read_backwards import FileReadBackwards
import calendar
import time
import glob
import os
import re
import hashlib
import modules.embed
import modules.usersData
import modules.serverData

# Class which handles and read the console.log file
class consoleReader(commands.Cog):

    def __init__(self, bot, logPath, dataPath):
        self.bot = bot
        self.logPath = logPath
        self.dataPath = dataPath
        self.lastMessageHash = None
        self.lastUpdateRealTimestamp = datetime.timestamp(datetime.now())*1000      
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
                                embed = self.handleLog(messageTimestamp, message, fromUpdate=True)
                                self.lastMessageHash = messageHash
                                if embed is not None and self.bot.channel is not None:
                                    await self.bot.channel.send(embed=embed)
                        else:
                            self.lastUpdateRealTimestamp = datetime.timestamp(datetime.now())*1000                   
                            break
                        


    # Parse a line in the server-console.txt file and take appropriate action

    def handleLog(self, timestamp: datetime, message: str, fromUpdate=False) -> Embed | None:
        self.bot.log.debug(f"consoleReader.py : Ignored : {message}")
   
 

