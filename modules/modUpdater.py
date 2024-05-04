from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
import os
from rcon.source import Client, rcon
import re
from datetime import datetime


class modUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkmodsupdate.start()
        self.rconHost = (
            os.getenv("RCON_HOST") if os.getenv("RCON_HOST") else "localhost"
        )
        port = os.getenv("RCON_PORT")
        if port is None:
            self.rconPort = 27015
            self.bot.log.info("Using default port")
        else:
            self.rconPort = int(port)
        self.rconPassword = os.getenv("RCON_PASSWORD")
    
    # checkmodsneedupdate
    # Bot command to check manually for mods update and restart the server if needed
    @commands.command()
    @has_permissions(administrator=True)
    async def checkmodsneedupdate(self, ctx):
        response = await rcon(
            "checkModsNeedUpdate",
            host=self.rconHost,
            port=self.rconPort,
            passwd=self.rconPassword,
        )
        self.bot.log.info("COMMAND: checkmodsneedupdate" + f" AUTHOR: {ctx.author}") 
    
    # Query the server every 5 mins to see if their is a mod update 
    @tasks.loop(minutes=5)
    async def checkmodsupdate(self):
        if not self.rconPassword:
            self.bot.log.warning("RCON password not set -- unable to checkModsNeedUpdate.")
            self.checkmodsupdate.stop()
            return
        self.bot.log.info("Checking rcon to see if mods need update")
        try:
            response = await rcon(
                "checkModsNeedUpdate",
                host=self.rconHost,
                port=self.rconPort,
                passwd=self.rconPassword,
            )
        except Exception as e:
            self.bot.log.error(e)
            self.bot.log.error(
                "Unable to run checkModsNeedUpdate command on rcon -- check rcon options"
            )
            self.checkmodsupdate.stop()
            return

