import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3
import random


class Select(discord.ui.Select):
	def __init__(self):
		options=[
			discord.SelectOption(label="Соль", value="1", emoji="🧂", description="Отпугнуть призрака |солью|"),
			discord.SelectOption(label="Крест", value="2", emoji="✝", description="Отпугнуть призрака |крестом|"),
			discord.SelectOption(label="Датчик движения", value="3", emoji="📡", description="Установить |Датчик Движения|"),
			discord.SelectOption(label="Датчик ЭМП", value="4", emoji="📳", description="проверить |ЭМП|"),
			discord.SelectOption(label="Камера", value="5", emoji="🎥", description="Установить |Камеры|"),
			discord.SelectOption(label="Книга", value="6", emoji="📖", description="Установить |Книгу|"),
			discord.SelectOption(label="Книга (Да/Нет)", value="7", emoji="📜", description="Установить |Да/Нет|"),
			discord.SelectOption(label="УФ-фонарик", value="8", emoji="🔦", description="Проверить на отпечатки рук"),
			discord.SelectOption(label="Успокоение", value="9", emoji="🎈", description="Успокоить призрака"),
			discord.SelectOption(label="Шкатулка", value="10", emoji="📻", description="Завести шкатулку призрака")
		]
		super().__init__(placeholder="Предметы", max_values=1, min_values=1, options=options)

	async def callback(self, interaction: discord.Interaction):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			one_use = cursor.execute(f"SELECT use_one FROM users WHERE id = ? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
			
			if one_use == 1:
				emb = discord.Embed( title =f"Вы уже использовали предмет!!", colour = discord.Color.red() )
			else:
				
				if self.values[0] == "1":
					salt = cursor.execute(f"SELECT salt FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if salt == 1:
						emb = discord.Embed( title =f"Вы использовали предмет соль!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET salt = salt - ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET salt_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "2":
					cross = cursor.execute(f"SELECT cross FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if cross == 1:
						emb = discord.Embed( title =f"Вы использовали предмет крест!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET cross = cross - ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET cross_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "3":
					sen1 = cursor.execute(f"SELECT sen1 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if sen1 == 1:
						emb = discord.Embed( title =f"Вы установили датчик движения!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET sen1 = ? WHERE id = ? AND server_id=?", (0, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET sen1_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id=?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "4":
					sen2 = cursor.execute(f"SELECT sen2 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if sen2 == 1:
						sen2_act = cursor.execute(f"SELECT sen2_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						min_sen2 = cursor.execute(f"SELECT agr FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						max_sen2 = cursor.execute(f"SELECT max_agr FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						emb = discord.Embed( title =f"Датчик активности показал: | {sen2_act} | \n Активность призрака: | {min_sen2}\\{max_sen2} |", colour = discord.Color.dark_teal() )
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )
				
				elif self.values[0] == "5":
					camera = cursor.execute(f"SELECT camera FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if camera == 1:
						emb = discord.Embed( title =f"Вы установили камеры!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET camera = ? WHERE id = ? AND server_id=?", (0, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET camera_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id=?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "6":
					item1 = cursor.execute(f"SELECT item1 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if item1 == 1:
						emb = discord.Embed( title =f"Вы установили пустую книгу на стол!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET item1 = ? WHERE id = ? AND server_id=?", (0, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET item1_g = ? WHERE server_id_bg=?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id=?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "7":
					item2 = cursor.execute(f"SELECT item2 FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if item2 == 1:
						emb = discord.Embed( title =f"Вы установили пустую книгу(да/нет) на стол!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET item2 = ? WHERE id = ? AND server_id=?", (0, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET item2_g = ? WHERE server_id_bg=?", (1, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id=?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						print(item2)
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "8":
					torch = cursor.execute(f"SELECT torch FROM users WHERE id=? AND server_id=?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if torch == 1:
						torch1 = cursor.execute(f"SELECT torch_g FROM bots_games WHERE server_id_bg=?", (interaction.user.guild.id,)).fetchone()[0]
						if torch1 == 1:
							emb = discord.Embed( title =f"Вы нашли отпечатки ног|рук призрака!!", colour = discord.Color.dark_teal() )
						else:
							emb = discord.Embed( title =f"Вы не нашли отпечатки ног|рук призрака!!", colour = discord.Color.brand_red() )
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	

				elif self.values[0] == "9":
					mw_1 = cursor.execute(f"SELECT mw_1 FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if mw_1 == 1:
						emb = discord.Embed( title =f"Вы использовали успокоение!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET mw_1 = mw_1 - ? WHERE server_id_bg = ?", (1, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				
				elif self.values[0] == "10":
					mw_2 = cursor.execute(f"SELECT mw_2 FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
					if mw_2 == 1:
						emb = discord.Embed( title =f"Вы использовали шкатулка!!", colour = discord.Color.dark_teal() )
						cursor.execute(f"UPDATE users SET mw_2 = mw_2 - ? WHERE server_id_bg = ?", (1, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE bots_games SET max_agr = max_agr - ? WHERE server_id_bg = ?", (20, interaction.user.id, interaction.user.guild.id,))
						cursor.execute(f"UPDATE users SET use_one = ? WHERE id = ? AND server_id = ?", (1, interaction.user.id, interaction.user.guild.id,))
					else:
						emb = discord.Embed( title =f"У вас нету такого предмета!!", colour = discord.Color.red() )	
				else:
					emb = discord.Embed( title =f"Такого предмета нету!!", colour = discord.Color.red() )	
				db.commit()
			await interaction.response.edit_message( embed = emb )
			db.commit()
		
		except sqlite3.Error as er:
			print(er)

		finally:
			cursor.close()
			db.close()

class SelectView(discord.ui.View):
	def __init__(self, *, timeout=30):
		super().__init__(timeout=timeout)
		self.add_item(Select())

class use_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "use_item", description="Поставить предмет")
	async def _use(self, interaction: discord.Interaction):
		await interaction.response.send_message("Выбери предмет для установки", view=SelectView(), ephemeral=True)


async def setup(bot):
	await bot.add_cog(use_games(bot))