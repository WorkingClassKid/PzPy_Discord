# PzPy

A discord bot for Project Zomboid. 

You are welcome to [log](https://github.com/WorkingClassKid/PzPy_Discord/issues) any issues, questions, or feature suggestions you have

## Features
- Beautiful Discord embed
- Multilingual (only bot messages sent to Discord are currently translatable)
  - Currently available in french and english
  - Feel free to provide your translated files!
  - Original .pot file for translating is in the locales directory
- Automatic mod updater available.
  - Can check if mods need to be updated every 5 mins
  - Send notification to the bot discord admin channel.
  - Save & Quit the server after 5 mins if mods updates are availables
  - Message the user (5 mins, 3 mins and 1 mins) on the server using the servermsg command. (Use the mod Unread Chat Notification + Classic IM Sound to be sure every users get the notifications)
  - Last warning 10 seconds before
  - Kick the remaining user out
  - Save and quit the server
  - Restart the server using a bash script (you need your own restart/monitor script).
- Mirror in-game chat messages to discord channel using linked discord name/avatar
- Notifications for logins, disconnects, deaths and perk changes
- Bot presence shows number of players currently online with plural support
- View and change server options
- [Skills Recovery Journal mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2503622437) support
  - Ignore sending level changes to discord channel when a user is reading a SRJ.
- Option to hide / display the timestamp
- Option to show the in-game chat with discord embed or not
- Compatible with server connected to Steam (not compatible with GOG (and will never be...))

## TO DO
- Log Extender mod complete support
- Options to choose witch data to send in the admin channel
- Make bot commands responses multilingual
- Better bot commands/responses
  - store users data per steamid to make !info and !users better
- Add other embed display options
- Send server online/offline message to the discord channel


## Commands (prefix: `!`):
```
RCONAdapter:
  option   Show or set the value of a server option
UserHandler:
  info     Get detailed user info
  users    Return a list of users on the server with basic info
No Category:
  help     Shows this message
```

## Requirements
- Python 3.9 and above should work
- Project Zomboid server / PzPy need to run on the same Linux dedicated server/vps
  - Tested on a dedicated server with Ubuntu
  - not tested on Windows and I will not support Windows. Make your own fork....

To install dependencies:
`pip install -r requirements.txt`

## Configuration
Configuration can be specified with an environment file named `.env`.
Sample configuration is provided in a file named `sample.env`. You can copy this file, name it `.env` and change the values to suit your environment.

#### Add yourself as an admin
- Edit the data/bot.admins file and add your discord username (in lowercase) in the file

## Running the bot
This bot works by monitoring the log files produced by the game, so must be run on the same machine as the server/host

To run:
`python PzPy.py`


It may be a good idea to run as a service, especially on a dedicated server

## Credits / Special Thanks

- Initialy forked from [Zomboi](https://github.com/JonnyPtn/zomboi/tree/master)
- [Chuckleberry-Finn](https://github.com/Chuckleberry-Finn) for updating his mod ([Skills Recovery Journal mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2503622437))  

## NOTICE
I'm not an expert programmer.... I program in my spare time for fun and I learn everything by myself.... I'm (not) sorry to the purists if the code is not optimal. But at least it works and I have fun making it :-)