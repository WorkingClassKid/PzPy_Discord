from datetime import datetime
from discord import Embed
from discord.ext import tasks, commands
from file_read_backwards import FileReadBackwards
import calendar
import time
import glob
import os
import re
import modules.embed
import modules.usersData
import modules.serverData

# Class which handles and read the console.log file
class consoleReader(commands.Cog):

    def __init__(self, bot, logPath, dataPath):
        self.bot = bot
        self.logPath = logPath
        self.dataPath = dataPath
        now = datetime.now()
        current_GMT = time.gmtime()
        self.lastUpdateRealTimestamp = calendar.timegm(current_GMT)
        self.loadHistory()
        self.update.start()

    def splitLine(self, line: str) -> tuple[datetime, str]:
        """Split a log line into a timestamp and the remaining message"""
        timestampStr, trash, message = line.strip()[1:].split(">", 2)
        # Ignore the start of the message before the timestamp
        timestampStr = timestampStr[timestampStr.find(",", 2) + 1 :]
        timestampStr = timestampStr.translate({ord(' '): None}) #fix unknown space issue
        message = message.translate({ord(' '): None}) #fix unknown space issue
        timestampStr = timestampStr[:-3] # remove the last 3 chars to make it 10 caracters
        return timestampStr, message

    @tasks.loop(seconds=2)
    async def update(self) -> None:
        files = glob.glob(os.getenv("PZ_PATH") + "/server-console.txt")

        if len(files) > 0:
            with FileReadBackwards(files[0]) as f:
                newTimestamp = self.lastUpdateRealTimestamp
                for line in f:
                    #self.bot.log.debug(line)
                    if "LOG" in line :
                        #self.bot.log.debug(line)
                        timestamp, message = self.splitLine(line)
                        timestamp = int(timestamp)
                        if timestamp > newTimestamp:
                            newTimestamp = timestamp
                        if timestamp > self.lastUpdateRealTimestamp:
                            embed = self.handleLog(timestamp, message, fromUpdate=True)
                            if embed is not None and self.bot.channel is not None:
                                await self.bot.channel.send(embed=embed)
                        else:
                            break
                    self.lastUpdateRealTimestamp = newTimestamp

    # Load the history from the files up until the last update time
    def loadHistory(self) -> None:
        self.bot.log.info("Loading Server Console history...")

        # Go through each user file in the log folder and subfolders
        files = glob.glob(self.logPath + "/**/*DebugLog-server.txt", recursive=True)
        files.sort(key=os.path.getmtime)
        #for file in files:
            #with open(file) as f:
                #for line in f:
                    #self.handleLog(*self.splitLine(line))

        self.bot.log.info("Server Console history loaded")

    # Parse a line in the user log file and take appropriate action

    def handleLog(self, timestamp: datetime, message: str, fromUpdate=False) -> Embed | None:
        self.bot.log.debug(f"Ignored: console.txt: {message}")
   
 

