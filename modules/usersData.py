import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)

class UsersData():
    def __init__(self, bot, logPath):
        self.bot = bot
        self.logPath = logPath
        
    
    # createUserDir - Create directory for the user data
    def createUserDir(self, dataPath, steamid):
        dataPath = os.path.join(dataPath, steamid)
        if not os.path.exists(dataPath):
            self.bot.log.warning(f"DATA directory is missing: {dataPath} . We will create it")
            os.makedirs(dataPath)
        if not os.path.exists(dataPath):
            self.bot.log.error(f"DATA directory is missing: {dataPath} . Unable to create it")
        else:
            self.bot.log.info(f"DATA directory exist: {dataPath}")
