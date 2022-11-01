import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3
import random

class item_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "inventory", description="Посмотреть свой инвентарь!")
	async def _item(self, interaction: discord.Interaction):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			salt = cursor.execute(f"SELECT salt FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			cross = cursor.execute(f"SELECT cross FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			sen1 = cursor.execute(f"SELECT sen1 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			sen2 = cursor.execute(f"SELECT sen2 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			camera = cursor.execute(f"SELECT camera FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			item1 = cursor.execute(f"SELECT item1 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			item2 = cursor.execute(f"SELECT item2 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			torch = cursor.execute(f"SELECT torch FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			mw_1 = cursor.execute(f"SELECT mw_1 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			mw_2 = cursor.execute(f"SELECT mw_2 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]

			emb = discord.Embed( title =f"ИНВЕНТАРЬ {interaction.user.name}!",description=f'Соль - {salt}\nКрест - {cross}\nДат.Движ - {sen1}\nДат.ЭМП - {sen2}\nКамера - {camera}\nКнига - {item1}\n(Да/Нет) - {item2}\nУФ-фонарик - {torch}\nУспокоение - {mw_1}\nШкатулка - {mw_2}' ,colour = discord.Color.blue() )
			await interaction.response.send_message( embed = emb, ephemeral=True )

		finally:
			cursor.close()
			db.close()


async def setup(bot):
	await bot.add_cog(item_games(bot))