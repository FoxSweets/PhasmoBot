import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
from discord.app_commands import Choice
import sqlite3

class Theend_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "theend", description="Выбрать призрака и закончить игру!")
	@app_commands.choices(ghost = [
		Choice(name = "Полтергейст", value = 1),
		Choice(name = "Демон", value = 2),
		Choice(name = "Тень", value = 3),
		Choice(name = "Мимик", value = 4),
		Choice(name = "Дух", value = 5),
		])
	async def _Theend(self, interaction: discord.Interaction, ghost: int):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			ghost1 = cursor.execute(f"SELECT Ghost FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			game1 = cursor.execute(f"SELECT games FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			if game1 == 0:
				emb = discord.Embed( title =f"Игра не началась!!", colour = discord.Color.red() )
				await interaction.response.send_message( embed = emb, ephemeral=True )
			else:
				activ = cursor.execute(f"SELECT activ_game FROM users WHERE id = ? AND server_id =? ", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
				if activ == 0:
					emb = discord.Embed( title =f"Вы не можете голосовать!!", colour = discord.Color.red() )
					await interaction.response.send_message( embed = emb, ephemeral=True )
				else:
					if ghost == 0:
						emb = discord.Embed( title =f"Выберите призрака (`/ghost`)!!", colour = discord.Color.red() )
						await interaction.response.send_message( embed = emb, ephemeral=True )
					else:
						server_id_gmp = cursor.execute(f"SELECT server_id_p FROM profile WHERE server_id_p = ?", (interaction.user.guild.id,)).fetchone()[0]
						ghost_name = cursor.execute(f"SELECT name FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
						if ghost == ghost1:
							emb = discord.Embed( title =f"Вы победили!! это был \"{ghost_name}\"", colour = discord.Color.teal() )

							cursor.execute(f"UPDATE profile SET win_p = win_p + ? WHERE server_id_p = ?", (1, server_id_gmp,))
							cursor.execute(f"UPDATE profile SET money_p = money_p + ? WHERE server_id_p = ?", (10, server_id_gmp,))
						else:
							emb = discord.Embed( title =f"Вы проиграли!! это был \"{ghost_name}\"", colour = discord.Color.dark_red() )
							cursor.execute(f"UPDATE profile SET lose_p = lose_p + ? WHERE server_id_p = ?", (1, server_id_gmp,))

						cursor.execute(f"UPDATE users SET cross = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET salt = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET sen1 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET sen2 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET camera = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET torch = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET item1 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET item2 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET mw_1 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET mw_2 = ? WHERE server_id = ?", (0,interaction.user.guild.id,))

						cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE server_id_p = ?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE profile SET server_id_p = ? WHERE server_id_p = ?", (0, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET players = ? WHERE server_id_bg = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET games = ? WHERE server_id_bg = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET activ_game = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET player = ? WHERE server_id = ?", (0,interaction.user.guild.id,))
						db.commit()
						await interaction.channel.send( embed = emb)
						emb = discord.Embed( title =f"Конец Игры!!", colour = discord.Color.blurple() )
						await interaction.response.send_message( embed = emb, ephemeral=True )
		finally:
			cursor.close()
			db.close()



async def setup(bot):
	await bot.add_cog(Theend_games(bot))