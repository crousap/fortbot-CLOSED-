import discord, json, os, asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from pytz import timezone

now = datetime.now()


colour = 0x39d0d6

link = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8"