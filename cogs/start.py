import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3
import random

class start_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "start", description="Начать игру!")
	async def _start(self, interaction: discord.Interaction):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			game1 = cursor.execute(f"SELECT games FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			if game1 == 1:
				emb = discord.Embed( title =f"Игра уже началась, подожди!!", colour = discord.Color.red() )
				await interaction.response.send_message(embed = emb, ephemeral=True)
			else:
				game = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
				if game == 0:
					emb = discord.Embed( title =f"Не хватает игроков!!", colour = discord.Color.red() )
				else:
					game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]

					emb = discord.Embed( title =f"ИГРА НАЧАЛАСЬ!!", colour = discord.Color.brand_green() )
					await interaction.response.send_message( embed = emb, ephemeral=False )
					cursor.execute(f"UPDATE bots_games SET games = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
					r1 = random.randint(1, 5)
					cursor.execute(f"UPDATE bots_games SET Ghost = ? WHERE server_id_bg = ?", (r1, interaction.user.guild.id,))
					r2 = random.randint(1, 3)
					cursor.execute(f"UPDATE bots_games SET age = ? WHERE server_id_bg = ?", (r2, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET max_agr = ? WHERE server_id_bg = ?", (100, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET sen1_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET camera_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET salt_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET cross_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET item1_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE bots_games SET item2_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE users SET use_one = ? WHERE server_id = ?", (0, interaction.user.guild.id,))
					cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE server_id_p = ?", (3, interaction.user.guild.id,))


					emb = discord.Embed( title = 'Предметы', colour = discord.Color.brand_green() )
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET salt = salt + ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Соль", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET cross = cross + ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Крест", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET sen1 = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Датчик движения", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET sen2 = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Датчик агрессии призрака", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET camera = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Камера", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET item1 = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Пустая книга", value = f"- игрок {play}", inline=False)
					play = random.randint(1, game4)
					cursor.execute(f"UPDATE users SET item2 = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="Книга (да/нет)", value = f"- игрок {play}", inline=False)
					cursor.execute(f"UPDATE users SET torch = ? WHERE player = ? AND server_id = ?", (1, play, interaction.user.guild.id,))
					emb.add_field(name="УФ-фонарик", value = f"- игрок {play}", inline=False)

				db.commit()
				await interaction.channel.send( embed = emb )
		
		finally:
			cursor.close()
			db.close()


async def setup(bot):
	await bot.add_cog(start_games(bot))