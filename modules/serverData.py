import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)
import modules.usersData

class UserStatus():
    def __init__(self, bot, dataPath):
        self.bot = bot
        
    
    # isOnline
    # Check if the user is online in data/online.users. If not, make it online
    def isOnline(self, dataPath, username, steamid):
        userData = username + ":" + steamid
        dataPath = os.path.join(dataPath, "online.users")
        # we check if the online.users file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.warning(f"serverData.py : online.users file is missing: {dataPath} . We will create it")
            file = open(dataPath, "w")
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"serverData.py :  online.users file is missing:: {dataPath} . Unable to create it")
        else:
          # we check if the username is in the online.users file and adjust the result accordingly
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content:
                    self.bot.log.info(f"serverData.py : (online.users) : {username} is already online")
                else:
                    self.bot.log.info(f"serverData.py : (online.users) : {username} is offline and should be online. Adjusting....")
                    with open(dataPath, 'a') as file:
                        file.write(f'{userData}\n')
                    with open(dataPath, 'r') as file:
                        content = file.read()
                    if username in content:
                        self.bot.log.info(f"serverData.py : (online.users): {username} is now online")
                    else:
                        self.bot.log.error(f"serverData.py : (online.users) : {username} is offline and should be online. Failed to adjust.")
                        
    
    # isOffline
    # Check if the user is offline in data/online.users. If not, make it offline
    def isOffline(self, dataPath, username):
        dataPath = os.path.join(dataPath, "online.users")
        # we check if the online.users file exist. if not we will create it
        if not os.path.isfile(dataPath):
            self.bot.log.warning(f"serverData.py : online.users file is missing: {dataPath} . We will create it")
            file = open(dataPath, "w")
        if not os.path.isfile(dataPath):
            self.bot.log.error(f"serverData.py : online.users file is missing:: {dataPath} . Unable to create it")
        else:
          # we check if the username is in the online.users file and adjust the result accordingly
            with open(dataPath, 'r') as file:
                content = file.read()
                if username in content:
                    self.bot.log.info(f"serverData.py : (online.users) : {username} is online and should be offline. Adjusting....")
                    with open(dataPath, "r") as file:
                        lines = file.readlines()
                    with open(dataPath, "w") as file:
                        for line in lines:
                            if username not in line.strip("\n"):
                                file.write(line)
                    with open(dataPath, 'r') as file:
                        content = file.read()            
                    if username in content:
                        self.bot.log.error(f"serverData.py : (online.users) : {username} is online and should be offline. Failed to adjust")
                    else:
                        self.bot.log.info(f"serverData.py : (online.users) : {username} is now offline")
    