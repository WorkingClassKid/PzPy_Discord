# PzPy

A discord bot for Project Zomboid. 

You are welcome to [log](https://github.com/WorkingClassKid/PzPy_Discord/issues) any issues, questions, or feature suggestions you have

## Features
- Beautiful Discord embed
- Multilingual (only bot messages sent to Discord are currently translatable)
  - Currently available in french and english
  - Feel free to provide your translated files!
  - Original .pot file for translating is in the locales directory
- Mirror in-game chat messages to discord channel using linked discord name/avatar
- Notifications for logins, disconnects, deaths and perk changes
- Bot presence shows number of players currently online with plural support
- View and change server options
- Request a map showing a players location (currently only work with vanilla map. no modded map support)
- [Skills Recovery Journal mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2503622437) support
- Option to hide / display the timestamp
- Option to show the in-game chat with discord embed or not
- Compatible with server connected to Steam (not compatible with GOG (and will never be...))

## TO DO
- Prevent people who reading Skills Recovery Journal to flood the discord channel with their skills upgrades (top priority)
- Options to choose witch data to send in the admin channel
- Make bot commands responses multilingual
- Better bot commands/responses
  - store users data per steamid to make !info and !users better
- Add other embed display options
- Ability to check for mods updates and if needed message the users and restart the server
- Send server online/offline message to the discord channel
- Update the MapHandler to support modded map (if possible and not before PZ build 42)(low priority)

# NOTICE
I'm not an expert programmer.... I program in my spare time for fun and I learn everything by myself.... I'm (not) sorry to the purists if the code is not optimal. But at least it works and I have fun making it :-)

## Commands (prefix: `!`):
```
MapHandler:
  location Get the last known location of the given user
RCONAdapter:
  option   Show or set the value of a server option
UserHandler:
  info     Get detailed user info
  users    Return a list of users on the server with basic info
No Category:
  help     Shows this message
```

## Requirements
Python 3.9 and above should work

To install dependencies:
`pip install -r requirements.txt`

## Configuration
Configuration can be specified using environment variables, which can also be declared using an environment file named `.env`.
Sample configuration is provided in a file named `sample.env`. You can copy this file, name it `.env` and change the values to suit your environment.

## Running the bot
This bot works by monitoring the log files produced by the game, so must be run on the same machine as the server/host

To run:
`python PzPy.py`

It may be a good idea to run as a service, especially on a dedicated server

## Credits

- Initialy forked from [Zomboi](https://github.com/JonnyPtn/zomboi/tree/master)