from discord import Embed, Colour
from datetime import datetime
from dotenv import load_dotenv
import os
import gettext

load_dotenv()

appname = 'zomboid_bot'
localedir = os.getenv("LANGUAGE_DIR")

# Set up Gettext
bot_translate = gettext.translation(appname, localedir, fallback=False, languages=['fr'])
bot_translate.install()


# Message formatting and coloring for public-facing logs


#def __embedify(timestamp: datetime, colour: Colour, message: str) -> Embed:
#   return Embed(timestamp=timestamp, colour=colour, description=message)

def __embedify(ShowTimestamp,timestamp: datetime, colour: Colour, message: str) -> Embed:
    if ShowTimestamp == "yes":
        return Embed(timestamp=timestamp, colour=colour, description=message)
                
    else:
        return Embed(timestamp=None, colour=colour, description=message)


# Chat Message

def chat_message(timestamp: datetime, message: str) -> Embed:
    """Stock blurple embed to relay a user's message"""
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.og_blurple(), message)

# Perk

def perk(timestamp: datetime, user: str, aka: str, perk: str, level: int) -> Embed:
    """Blue embed to indicate a user's level-up"""
    message = f":chart_with_upwards_trend: {user} {aka}reached {perk} level {level}"
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.og_blue(), _("LEVEL_UP_MESSAGE"))

# Join

def join(timestamp: datetime, user: str, aka: str) -> Embed:
    """Green embed to indicate a new user/character joining"""
    return __embedify(timestamp, Colour.green(), _("JOIN_MESSAGE"))

# Resume

def resume(timestamp: datetime, user: str, aka: str, hours: int) -> Embed:
    """Green embed to indicate a user/character resuming"""
    message = f":person_doing_cartwheel: {user} {aka}has arrived, survived for {hours} hours so far..." + _("ARRIVAL_MESSAGE")
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.green(), message)

# Leave

def leave(timestamp: datetime, user: str) -> Embed:
    """Red embed to indicate a user disconnecting"""
    message = f":person_running: {user} has left"
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.red(), _("LEFT_MESSAGE"))

# Death 

def death(timestamp: datetime, user: str, aka: str, hours: int) -> Embed:
    """Dark embed to indicate a user's/character's death"""
    message = f":zombie: {user} {aka}died after surviving {hours} hours :dizzy_face:"
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.dark_red(), _("DIED_MESSAGE"))

# Skill Recovery Journal

def srj(timestamp: datetime, user: str, aka: str, hours: int) -> Embed:
    """Gold embed to indicate a user reading is skill journal"""
    message = f":book: {log_char_string} (**{user.name}**) fait un peu de lecture......."
    return __embedify(os.getenv("SHOW_TIMESTAMP"), timestamp, Colour.gold(), _("SRJ_MESSAGE"))
