import discord, random, os, asyncio, json
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from pytz import timezone


colour = 0x39d0d6   # Цвет который используется по умолчанию в embed
link = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8"   # Ссылка на приглашение бота
adm_help = ["info", "say"]  # Админские команды которые не будут показываться при написании $help
cfg = json.load(open('cfg.json', 'r'))
