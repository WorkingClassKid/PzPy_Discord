# PzPy-Discord

A discord bot for Project Zomboid. 

Initialy forked from https://github.com/JonnyPtn/zomboi/tree/master

You are welcome to [log](https://github.com/buttsbucket/zomboi_bot/issues) any issues, questions, or feature suggestions you have

## Features
- Mirror in-game chat messages to discord channel using linked discord name/avatar
- Notifications for logins, disconnects, deaths and perk changes
- Presence shows number of players currently online
- View and change server options
- Request a map showing a players location
- [Skills Recovery Journal mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2503622437) ([Github](https://github.com/Chuckleberry-Finn/Skill-Recovery-Journal)) support
- Option to hide / display the timestamp
- Option to show the chat with discord embed or not

## TO DO
- Multilingual (currently only available in french... English available soon)
- Make bot commands multilingual. 
- Update the MapHandler to support modded map (if possible)

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
Python 3.8 and above should work

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

