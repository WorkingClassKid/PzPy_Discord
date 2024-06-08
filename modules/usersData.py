import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)

class UsersData():
    def __init__(self, bot, logPath):
        self.bot = bot
        self.logPath = logPath
        self.botOwner = os.getenv("BOT_OWNER")
        
    
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
            
    # isAdmin
    # Check if a user is a bot administrator 
    # Return True or False
    def isAdmin(self, dataPath, username):
        dataPath = os.path.join(dataPath, "bot.admins")
        username = username
        # we check if the bot.admins file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"userData.py : isAdmin : bot.admins file is missing:: {dataPath} .")
            return False
        else:
          # we check if the username is in the bot.admins file
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content or username == self.botOwner:
                    return True
                else:
                    return False

    # srjStartReading
    # Add user in data/srj.reading file when user start reading a skill recovery journal
    def srjStartReading(self, dataPath, username, start_timestamp):
        start_timestamp = str(start_timestamp)
        userData = username + ":" + start_timestamp
        dataPath = os.path.join(dataPath, "srj.reading")
        # we check if the srj.reading file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.warning(f"userData.py : srj.reading file is missing: {dataPath} . We will create it")
            file = open(dataPath, "w")
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"userData.py :  srj.reading file is missing:: {dataPath} . Unable to create it")
        else:
          # we check if the username is in the data/srj.reading file and adjust the result accordingly
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content:
                    self.bot.log.info(f"userData.py : srjStartReading : {username} is already in srj.reading")
                else:
                    self.bot.log.info(f"userData.py : srjStartReading : {username} is not in srj.reading and it should be. Adjusting....")
                    with open(dataPath, 'a') as file:
                        file.write(f'{userData}\n')
                    with open(dataPath, 'r') as file:
                        content = file.read()
                    if username in content:
                        self.bot.log.info(f"userData.py : srjStartReading : {username} is now reading is Skill Recovery Journal")
                    else:
                        self.bot.log.error(f"userData.py : srjStartReading : {username} is not in srj.reading and it should be. Failed to adjust.")
                      
                      
    # srjStopReading
    # Remove user in data/srj.reading file when user stop reading a skill recovery journal
    def srjStopReading(self, dataPath, username):
        dataPath = os.path.join(dataPath, "srj.reading")
        # we check if the srj.reading file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.warning(f"userData.py : srjStopReading : srj.reading file is missing: {dataPath} . We will create it")
            file = open(dataPath, "w")
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"userData.py : srjStopReading : srj.reading file is missing:: {dataPath} . Unable to create it")
        else:
          # we check if the username is in the srj.reading file and adjust the result accordingly
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content:
                    self.bot.log.info(f"userData.py : srjStopReading : {username} is in srj.reading but as stopped reading the srj. Adjusting....")
                    with open(dataPath, "r") as file:
                        lines = file.readlines()
                    with open(dataPath, "w") as file:
                        for line in lines:
                            if username not in line.strip("\n"):
                                file.write(line)
                    with open(dataPath, 'r') as file:
                        content = file.read()            
                    if username in content:
                        self.bot.log.error(f"userData.py : srjStopReading : {username} is in srj.reading but as stopped reading his skill recovery journal. Failed to adjust")
                    else:
                        self.bot.log.info(f"userData.py : srjStopReading : {username} as stopped reading his skill recovery journal")
                        
                        
                        
    # isSrjReading
    # Check if a user is reading is skill recovery journal. 
    # Return True or False
    def isSrjReading(self, dataPath, username):
        dataPath = os.path.join(dataPath, "srj.reading")
        # we check if the srj.reading file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.warning(f"userData.py : isSrjReading : srj.reading file is missing: {dataPath} . We will create it")
            file = open(dataPath, "w")
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"userData.py : isSrjReading : srj.reading file is missing:: {dataPath} . Unable to create it")
            return False
        else:
          # we check if the username is in the srj.reading file and adjust the result accordingly
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content:
                    with open(dataPath, "r") as file:
                        lines = file.readlines()
                        # if username is in srj.reading file, we split the username and timestamp
                        for line in lines:
                            if username in line.strip("\n"):
                                srj_username, srj_timestamp = line.split(":")
                                srj_timestamp = float(srj_timestamp)
                                # we check if the timestamp is more than 5 minutes
                                new_timestamp = datetime.now().timestamp()
                                if srj_timestamp < new_timestamp: 
                                    # if the timestamp is more than 5 minutes, we return False and delete the line for that user in sjr.reading            
                                    with open(dataPath, "r") as file:
                                        lines = file.readlines()
                                    with open(dataPath, "w") as file:
                                        for line in lines:
                                            if username not in line.strip("\n"):
                                                file.write(line)
                                        self.bot.log.debug(f"userData.py : isSrjReading : FALSE: {username} is in srj.reading for more than 5 minutes. User removed from srj.reading")
                                        return False
                                else:
                                    # if timestamp is less than 5 minutes, we return True
                                    self.bot.log.debug(f"userData.py : isSrjReading : TRUE: {username} is in srj.reading for less 5 minutes. Skipping message to discord channel")
                                    return True
                else:
                 # if username is not in sjr.reading file return False
                    self.bot.log.debug(f"userData.py : isSrjReading : FALSE: {username} is not in srj.reading")
                    return False
            