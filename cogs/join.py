import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3

class join_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@app_commands.command(name = "join", description="Присоединиться к игре")
	async def _join(self, interaction: discord.Interaction):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			if cursor.execute(f"SELECT server_id_bg FROM bots_games WHERE server_id_bg=?", (interaction.user.guild.id,)).fetchone() is None:
				cursor.execute(f"INSERT INTO bots_games VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.guild.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))
				db.commit()

			game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			activ = cursor.execute(f"SELECT games FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			update = cursor.execute(f"SELECT id_up FROM 'update'").fetchone()[0]
			

			if activ == 1:
				emb = discord.Embed( title =f"Игра уже началась!!", colour = discord.Color.red() )
			else:
				if game4 > 5:
					emb = discord.Embed( title =f"Комната переполнена", colour = discord.Color.green() )
				else:
					if cursor.execute(f"SELECT id FROM users WHERE server_id = {interaction.user.guild.id} AND id={interaction.user.id}").fetchone() is None:
						cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)", (interaction.user.guild.id, interaction.user.id, interaction.user.name, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))
						if cursor.execute(f"SELECT id_p FROM profile WHERE id_p={interaction.user.id}").fetchone() is None:
							cursor.execute(f"INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.guild.id, 2, interaction.user.id, interaction.user.name, update, 0, 0, 0, 0, 0, 0, 0, 0,))
						else:
							cursor.execute(f"UPDATE profile SET server_id_p = ? WHERE id_p = ?", (interaction.user.guild.id, interaction.user.id,))
							cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE id_p = ?", (2, interaction.user.id,))
						db.commit()
						cursor.execute(f"UPDATE bots_games SET players = players + 1 WHERE server_id_bg = ?", (interaction.user.guild.id,))
						playr1 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						cursor.execute(f"UPDATE users SET player = ? WHERE id = ? AND server_id = ?", (playr1, interaction.user.id, interaction.user.guild.id,))
						game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						emb = discord.Embed( title =f"Вы присоединились в свою первую комнату на данном сервере!! ({game4}/4)", colour = discord.Color.gold() )
					else:
						game = cursor.execute(f"SELECT activ_game FROM users WHERE id = {interaction.user.id} AND server_id = {interaction.user.guild.id}", ).fetchone()[0]
						if game == 0:
							action = cursor.execute(f"SELECT action_on_p FROM profile WHERE id_p = ?", (interaction.user.id,)).fetchone()[0]
							if action == 2:
								emb = discord.Embed( title =f"Вы уже в ***лобби*** на другом сервере!!", colour = discord.Color.red() )
							elif action == 3:
								emb = discord.Embed( title =f"Вы уже в ***играете*** на другом сервере!!", colour = discord.Color.red() )
							else:
								cursor.execute(f"UPDATE profile SET server_id_p = ? WHERE id_p = ?", (interaction.user.guild.id, interaction.user.id,))
								cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE id_p = ?", (2, interaction.user.id,))
								cursor.execute(f"UPDATE bots_games SET players = players + 1 WHERE server_id_bg = ?", (interaction.user.guild.id,))
								cursor.execute(f"UPDATE users SET activ_game = ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
								playr1 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
								cursor.execute(f"UPDATE users SET player = ? WHERE id = ? AND server_id = ?", (playr1, interaction.user.id, interaction.user.guild.id,))
								game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
								update_later = cursor.execute(f"SELECT update_p FROM profile WHERE id_p = ?", (interaction.user.id,)).fetchone()[0]
								
								emb = discord.Embed( title =f"{interaction.user.name} присоединился в комнату!! ({game4}/4)", colour = discord.Color.gold() )
								await interaction.channel.send( embed = emb )
								if update == update_later:
									emb = discord.Embed( title =f"Удачной игры", colour = discord.Color.teal() )
								else:
									date_update = cursor.execute(f"SELECT date_up FROM 'update'").fetchone()[0]
									emb = discord.Embed( title =f"Обнова |{update}| от ({date_update})",description = "За ваще отсутсвие произошли изменения, пропишите `/update` и посмотрите обнову!", colour = discord.Color.magenta() )
						else:
							emb = discord.Embed( title =f"Вы уже в игре!!", colour = discord.Color.red() )
			await interaction.response.send_message( embed = emb, ephemeral=True )
			db.commit()
		finally:
			cursor.close()
			db.close()


async def setup(bot):
	await bot.add_cog(join_games(bot))