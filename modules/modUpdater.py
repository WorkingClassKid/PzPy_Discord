import discord
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
import os
from rcon.source import Client, rcon
import re
from datetime import datetime
import modules.usersData
import asyncio
import subprocess   

class modUpdater(commands.Cog):

    def __init__(self, bot, dataPath):
        self.bot = bot
        self.dataPath = dataPath
        self.botOwner = os.getenv("BOT_OWNER")
        self.checkmodsupdate.start()
   
    # startUpdate
    # Start the mods update process
    async def startUpdate(self):
        self.bot.log.info("modUpdater.py : startUpdate : Mod update is starting")
        self.bot.log.info("modUpdater.py : Update Started : Server will restart in 5 mins")
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Mods updates is starting")
        # send a message to the user 5 mins before the reboot
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Restart in 5 minutes")
        response = await rcon(
            "servermsg \" " + _("MOD_UPDATER_UPDATE_REQUIRED") + "\"",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(120)
        # send a message to the user 3 mins before the reboot
        self.bot.log.info("modUpdater.py : Mods Update : Server will restart in 3 mins")
        response = await rcon(
            "servermsg \" " + _("MOD_UPDATER_UPDATE_REQUIRED_3MINS") + "\"",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(120)
        # send a message to the user 1 mins before the reboot
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Restart in 1 minutes")
        self.bot.log.info("modUpdater.py : Mods Update : Server will restart in 1 mins")
        response = await rcon(
            "servermsg \" " + _("MOD_UPDATER_UPDATE_REQUIRED_1MINS") + "\"",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(60)
        
        # Last warning. 10 seconds before reboot
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Restart in 10 seconds")
        self.bot.log.info("modUpdater.py : Mods Update : Server will restart in 10 seconds")
        response = await rcon(
            "servermsg \" " + _("MOD_UPDATER_UPDATE_REQUIRED_10SEC") + "\"",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(10)
        
        # Kick remaining user
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Kicking remaining users")
        self.bot.log.info("modUpdater.py : Mods Update : Kick remaining users")
        file = open(os.getenv("DATA_PATH") + '/online.users', 'r')
        lines = file.readlines()
        for line in lines:
            username, steamid = line.split(":")
            response = await rcon(
            "kickuser \"" + username + "\"-r \"Server Update\"",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        # emptying online.users file
        open(os.getenv("DATA_PATH") + '/online.users', 'w').close()

        # Save
        await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Save & Shutdown")
        self.bot.log.info("modUpdater.py : Mods Update : Save")
        response = await rcon(
            "save",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(10)
        
        # Quit
        self.bot.log.info("modUpdater.py : Mods Update : Quit")
        response = await rcon(
            "quit",
            host=os.getenv("RCON_HOST"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PASSWORD"),
        )
        await asyncio.sleep(10)
        
        # Reboot script
        isFile = os.path.isfile(os.getenv("MOD_UPDATE_REBOOT_SCRIPT"))
        if isFile:
            await self.adminChannel.send(f"PzPy : modUpdater.py : CheckModsNeedUpdate : Reboot script found. Trying to use it...")
            self.bot.log.info("modUpdater.py : CheckModsNeedUpdate : Reboot script found. Trying to use it...")
            subprocess.call(os.getenv("MOD_UPDATE_REBOOT_SCRIPT"))
            
        self.bot.log.info("modUpdater.py : CheckModsNeedUpdate : Reboot in progress. Sleeping for 4 mins.")
        await asyncio.sleep(240)
        
        
        
    # checkmodsneedupdate
    # Bot command to check manually for mods update and restart the server if needed
    @commands.command()
    async def checkmodsneedupdate(self, ctx):
        author = str(ctx.author)
        self.bot.log.info("modUpdater.py : BOT COMMAND : checkmodsneedupdate " + f": {author}")
        if modules.usersData.UsersData.isAdmin(self, self.dataPath, author):
            response = await rcon(
                "checkModsNeedUpdate",
                host=os.getenv("RCON_HOST"),
                port=os.getenv("RCON_PORT"),
                passwd=os.getenv("RCON_PASSWORD"),
            )
            self.bot.log.info("modUpdater.py : BOT COMMAND : checkmodsneedupdate " + f": {ctx.author}")
            if "Checking started" in response :
                await ctx.send(f"PzPy : modUpdater.py : Mods Update Check: Started")
    
    # Query the server automaticaly every 5 mins to see if their is a mod update 
    @tasks.loop(minutes=5)
    async def checkmodsupdate(self):
        if not os.getenv("RCON_PASSWORD"):
            self.bot.log.warning("modUpdater.py : ERROR : RCON password not set -- unable to checkModsNeedUpdate.")
            self.checkmodsupdate.stop()
            return
        self.bot.log.info("modUpdater.py : TASKS : Checking if mods need update")
        try:
            response = await rcon(
                "checkModsNeedUpdate",
                host=os.getenv("RCON_HOST"),
                port=os.getenv("RCON_PORT"),
                passwd=os.getenv("RCON_PASSWORD"),
            )
        except Exception as e:
            self.bot.log.error(e)
            self.bot.log.error("modUpdater.py : TASKS :  Unable to run checkModsNeedUpdate command on rcon -- check rcon configuration")
            self.checkmodsupdate.stop()
            return
            
            
            

