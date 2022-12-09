import config
import discord
from discord.ext import commands
from db import *
import os

PREFIX = ["Ph.", "ph."]
bot = commands.Bot(command_prefix= PREFIX,help_command=None, intents = discord.Intents.all())

#--------------------------------------
# bot event online
@bot.event
async def on_ready():
	print()
	print('Бот в онлайне')
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')
			print(f"Загружен файл - |{filename[:-3]}|")
	await bot.tree.sync()

#-------------------------------------------------
# bot run
bot.run(config.TOKEN)