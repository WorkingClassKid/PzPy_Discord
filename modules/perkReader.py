import time, datetime
from datetime import datetime, timedelta
from discord import Embed
from discord.ext import tasks, commands
from file_read_backwards import FileReadBackwards
import glob
import os
import re
import modules.embed
import modules.usersData
import modules.serverData

class perkReader(commands.Cog):
    """Class which handles the Perk log files"""

    def __init__(self, bot, logPath, dataPath):
        self.bot = bot
        self.logPath = logPath
        self.dataPath = dataPath
        self.lastUpdateTimestamp = datetime.now()
        self.loadHistory()
        self.update.start()
        self.notifyJoin = os.getenv("JOINS", "True") == "True"
        self.notifyDeath = os.getenv("DEATHS", "True") == "True"
        self.notifyPerk = os.getenv("PERKS", "True") == "True"
        self.notifyCreateChar = os.getenv("CREATECHAR", "True") == "True"

    def splitLine(self, line: str) -> tuple[datetime, str]:
        """Split a log line into a timestamp and the remaining message"""
        timestampStr, message = line.strip()[1:].split("]", 1)
        timestamp = datetime.strptime(timestampStr, "%d-%m-%y %H:%M:%S.%f")
        return timestamp, message

    @tasks.loop(seconds=2)
    async def update(self) -> None:
        files = glob.glob(self.logPath + "/*PerkLog.txt")
        if len(files) > 0:
            with FileReadBackwards(files[0]) as f:
                newTimestamp = self.lastUpdateTimestamp
                for line in f:
                    timestamp, message = self.splitLine(line)
                    if timestamp > newTimestamp:
                        newTimestamp = timestamp
                    if timestamp > self.lastUpdateTimestamp:
                        embed = self.handleLog(timestamp, message, fromUpdate=True)
                        if embed is not None and self.bot.channel is not None:
                            await self.bot.channel.send(embed=embed)
                    else:
                        break
                self.lastUpdateTimestamp = newTimestamp

    # Load the history from the files up until the last update time
    def loadHistory(self) -> None:
        self.bot.log.info("perkReader.py : Loading Perk history...")

        # Go through each user file in the log folder and subfolders
        files = glob.glob(self.logPath + "/**/*PerkLog.txt", recursive=True)
        files.sort(key=os.path.getmtime)
        for file in files:
            with open(file) as f:
                for line in f:
                    self.handleLog(*self.splitLine(line))

        self.bot.log.info("perkReader.py : Perk history loaded")

    # Parse a line in the user log file and take appropriate action

    def handleLog(self, timestamp: datetime, message: str, fromUpdate=False) -> Embed | None:
        # SteamID - We search for the steamid
        steamid, trash = message.split("]", 1)
        steamid = steamid.translate({ord('['): None})
        steamid = steamid.translate({ord(' '): None}) #fix unknown space issue
        # Ignore the id at the start of the message, no idea what it's for
        message = message[message.find("[", 2) + 1 :]

        # Next is the name which we use to get the user
        name, message = message.split("]", 1)
        userHandler = self.bot.get_cog("userReader")
        user = userHandler.getUser(name)
        char_name = userHandler.getCharName(name) if fromUpdate and user else None
        log_char_string =  char_name if char_name else ""

        # Then position which we set if it's more recent
        x = message[1 : message.find(",")]
        y = message[message.find(",") + 1 : message.find(",", message.find(",") + 1)]
        message = message[message.find("[", 2) + 1 :]

        if timestamp > user.lastSeen:
            user.lastSeen = timestamp
            user.lastLocation = (x, y)
        avatar = "https://raw.githubusercontent.com/WorkingClassKid/Divers/master/BrawlerSpiffo.png"
        # Then the message type, can be "Died", "Login", "Level Changed" or a list of perks
        type, message = message.split("]", 1)

        # Skill Recovery Journal FIX
        if type != "SRJ START READING" and type != "SRJ STOP READING":
            hours = re.search(r"Hours Survived: (\d+)", message).group(1)
            user.hoursAlive = hours
            if int(hours) > int(user.recordHoursAlive):
                user.recordHoursAlive = hours


        if type == "Died":
            user.died.append(timestamp)
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"perkReader.py : Died : {user.name}")
                if self.notifyDeath:
                    for member in self.bot.get_all_members():
                        self.bot.log.debug(f"perkReader.py : Died: discord username: {member}") # debug show discord channel member
                            
                        if user.name.lower() in member.name:
                            avatar = member.display_avatar
                            
                            self.bot.log.debug(f"perkReader.py : Died : --------MATCH--------") # degug show the username match with discord 
                        else:
                            self.bot.log.debug(f"perkReader.py : Died : no match")  # degug show their is no match with discord
                                
                    self.bot.log.debug(f"perkReader.py : Died : avatarurl : {avatar}") # degug show avatar url
                        
                    return modules.embed.death(
                        timestamp, user.name, log_char_string, avatar, user.hoursAlive
                    )

        elif type == "Login":
            if timestamp > self.lastUpdateTimestamp:
                user.online = True
                self.bot.log.debug(f"LOGIN USERNAME: {user.name.lower()}") # debug show the username who resume is game
                if self.notifyJoin:
                    # we check in the discord channel for a username match
                    for member in self.bot.get_all_members():
                    
                        self.bot.log.debug(f"perkReader.py : Login : discord username: {member}") # debug show discord channel member
                            
                        if user.name.lower() in member.name:
                            avatar = member.display_avatar
        
                            self.bot.log.debug(f"perkReader.py : Login : --------MATCH--------") # degug show the username match with discord
                                
                        else:
                            self.bot.log.debug(f"perkReader.py : Login : no match") # degug show their is no match with discord
                                
                    self.bot.log.debug(f"perkReader.py : Login : avatarurl : {avatar}") # degug show avatar url
               
                    return modules.embed.resume(
                        timestamp, user.name, log_char_string, avatar, user.hoursAlive)

        elif "Created Player" in type:
            if timestamp > self.lastUpdateTimestamp:
                user.online = True
                self.bot.log.info(f"perkReader.py : new character : {user.name}")
                

                self.bot.log.info(f"perkReader.py : Created Player : player PZ username : {user.name.lower()}") # debug show the username who created a player
                
                if self.notifyCreateChar:
                    for member in self.bot.get_all_members():
                    
                        self.bot.log.debug(f"perkReader.py : Created Player : discord username : {member}")  # debug show discord channel member
                            
                        if user.name.lower() in member.name:
                            avatar = member.display_avatar
                            
                            self.bot.log.debug(f"perkReader.py : Created Player : --------MATCH--------")  # degug show the username match with discord
                                 
                        else:
                            self.bot.log.debug(f"perkReader.py : Created Player : no match") # degug show their is no match with discord
                                

                    self.bot.log.debug(f"perkReader.py : Created Player : avatarurl : {avatar}") # degug show avatar url
                    
                return modules.embed.join(timestamp, user.name, log_char_string, avatar)

        elif type == "Level Changed":
            match = re.search(r"\[(\w+)\]\[(\d+)\]", message)
            perk = match.group(1)
            level = match.group(2)
            user.perks[perk] = level
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"perkReader.py : Level Changed : {user.name} {perk} changed to {level}")
                self.bot.log.debug(f"perkReader.py : Level Changed : {user.name.lower()}") # debug show the username who changed perk
                if self.notifyPerk and not modules.usersData.UsersData.isSrjReading(self, self.dataPath, user.name):
                    for member in self.bot.get_all_members():
                        self.bot.log.debug(f"perkReader.py : Level Changed : discord username : {member}") # debug show discord channel member
                        if user.name.lower() in member.name:
                            avatar = member.display_avatar
                            self.bot.log.debug(f"perkReader.py : Level Changed : --------MATCH--------") # degug show the username match with discord
                        else:
                            self.bot.log.debug(f"perkReader.py : Level Changed : no match") # degug show their is no match with discord
                    
                        self.bot.log.debug(f"perkReader.py : Level Changed : avatarurl {avatar}")  # degug show avatar url
                        
                    return modules.embed.perk(
                        timestamp, user.name, log_char_string, avatar, perk, level
                    )
                else:
                    self.bot.log.debug(f"perkReader.py : IGNORED : Level Changed : {user.name} {perk} changed to {level}") # debug ignored perk change
                        
                        
     # Skill Recovery Journal Support
        elif type == "SRJ START READING":
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"perkReader.py : Skill Recovery Journal : Start : {user.name}")
                start_timestamp = datetime.now() + timedelta(minutes = 5)
                start_timestamp = start_timestamp.timestamp()
                modules.usersData.UsersData.srjStartReading(self, self.dataPath, user.name, start_timestamp)
                return modules.embed.srj(
                        timestamp, user.name, log_char_string
                    )
        elif type == "SRJ STOP READING":
            if timestamp > self.lastUpdateTimestamp:
                self.bot.log.info(f"perkReader.py : Skill Recovery Journal : Stop : {user.name}")
                modules.usersData.UsersData.srjStopReading(self, self.dataPath, user.name)

        else:
            # Must be a list of perks following a login/player creation
            for name, value in re.findall(r"(\w+)=(\d+)", type):
                user.perks[name] = value
