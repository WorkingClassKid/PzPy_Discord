import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)

class UsersData():
    def __init__(self, bot, logPath):
        self.bot = bot
        self.logPath = logPath
        
    
    # createUserDir
    # Create directory for the user data
    def createUserDir(self, dataPath, username):
        dataPath = os.path.join(dataPath, username)
        if not os.path.exists(dataPath):
            self.bot.log.warning(f"userData.py : ERROR : user data directory is missing: {dataPath} . We will create it")
            os.makedirs(dataPath)
        if not os.path.exists(dataPath):
            self.bot.log.error(f"userData.py : ERROR : user data directory is missing: {dataPath} . Unable to create it")
        else:
            self.bot.log.info(f"userData.py : user data directory exist: {dataPath}")

    # createSteamid
    # Create the steamid file in the user data directory
    def createSteamidFile(self, dataPath, username, steamid):
        steamidPath = os.path.join(dataPath, username, "steamid")
        if not os.path.isfile(steamidPath):
            self.bot.log.warning(f"userData.py : ERROR : steamid file for {username} is missing: {steamidPath} . We will create it")
            steamidFile = open(steamidPath, "x")
            steamidFile.write(steamid)
        if not os.path.isfile(steamidPath):
            self.bot.log.error(f"userData.py : ERROR : steamid file for {username} is missing: {steamidPath} . Unable to create it")
        else:
            self.bot.log.info(f"userData.py : steamid file for {username} exist: {steamidPath}")
