import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3
import random
import asyncio

class end_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "end", description="закончить раунд!")
	async def _end(self, interaction: discord.Interaction):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			ghost1 = cursor.execute(f"SELECT Ghost FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			game1 = cursor.execute(f"SELECT games FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			age1 = cursor.execute(f"SELECT age FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
			sen2_nz = cursor.execute(f"SELECT sen2_item FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
			sen2_ran = random.randint(3, sen2_nz)
			if game1 == 0:
				emb = discord.Embed( title =f"Игра не началась!!", colour = discord.Color.red() )
				await interaction.response.send_message( embed = emb, ephemeral=True )
			else:
				activ = cursor.execute(f"SELECT activ_game FROM users WHERE id = ? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
				if activ == 0:
					emb = discord.Embed( title =f"Вы не можете скипнуть действия!!", colour = discord.Color.red() )
					await interaction.response.send_message( embed = emb, ephemeral=True )
				else:
					emb = discord.Embed( title =f"Дальше ходит призрак!!", colour = discord.Color.orange() )
					await interaction.response.send_message( embed = emb, ephemeral=False )
					await asyncio.sleep(1*1)
					agr_level1 = cursor.execute(f"SELECT agr_level FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
					if agr_level1 == 1:
						salt1 = cursor.execute(f"SELECT salt_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						if salt1 == 1:
							emb = discord.Embed( title =f"Не кто не убит, вас спасла соль!!", colour = discord.Color.brand_green() )
							cursor.execute(f"UPDATE bots_games SET salt_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
							cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
							cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
							cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
						else:
							cross1 = cursor.execute(f"SELECT cross_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
							if cross1 == 1:
								emb = discord.Embed( title =f"Не кто не убит, вас спас крест!!", colour = discord.Color.brand_green() )
								cursor.execute(f"UPDATE bots_games SET cross_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
							else:
								game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
								game4 = game4 + 1
								r_kill = random.randint(1, game4)
								print("Минус:", r_kill)
								if r_kill == 1:
									emb = discord.Embed( title =f"Не кто не умер!!", colour = discord.Color.brand_green() )
									cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
								else:
									game4 = game4 - 1
									id_pl = cursor.execute(f"SELECT id FROM users WHERE player = ?", (game4,)).fetchone()[0]
									
									cursor.execute(f"UPDATE users SET cross = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET salt = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET sen1 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET sen2 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET camera = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET torch = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET item1 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET item2 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET mw_1 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))
									cursor.execute(f"UPDATE users SET mw_2 = ? WHERE server_id = ? AND player = ?", (0,interaction.user.guild.id, game4,))

									cursor.execute(f"UPDATE profile SET lose_p = lose_p + ? WHERE id_p = ? AND server_id_p = ?", (1, id_pl, interaction.user.guild.id,))
									cursor.execute(f"UPDATE users SET activ_game = ? WHERE player = ? AND server_id = ?", (0, game4, interaction.user.guild.id,))
									cursor.execute(f"UPDATE users SET player = ? WHERE player = ? AND server_id = ?", (0, game4, interaction.user.guild.id,))
									cursor.execute(f"UPDATE bots_games SET players = players - ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
									emb = discord.Embed( title =f"Игрок {game4} покидает наш мир!!", colour = discord.Color.default() )
									cursor.execute(f"UPDATE profile SET server_id_p = ? WHERE id_p = ?", (0, id_pl,))
									cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE id_p = ?", (1, id_pl,))
									cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									cursor.execute(f"UPDATE bots_games SET agr = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									db.commit()
									player = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
									if player == 0:
										await interaction.channel.send( embed = emb )
										emb = discord.Embed( title =f"ИГРА ОКОНЧЕНА!!", colour = discord.Color.dark_red() )
										cursor.execute(f"UPDATE bots_games SET games = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))								
					else:
						agr1 = cursor.execute(f"SELECT agr FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						max_sen2 = cursor.execute(f"SELECT max_agr FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
						if agr1 >= max_sen2:
							agr2 = 100
						else:
							agr2 = random.randint(agr1, max_sen2)
							print("атака:", agr2)
						
						if agr2 >= 95:
							emb = discord.Embed( title =f"НАЧАЛАСЬ ФАЗА АТАКИ ПРИЗРАКА!!", colour = discord.Color.brand_red() )
							cursor.execute(f"UPDATE bots_games SET agr_level = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
							cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_nz, interaction.user.guild.id,))
						else: #--------------------Дальше не трогать-----------------
							max_sen2 = cursor.execute(f"SELECT max_agr FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
							
							if max_sen2 != 100:
								cursor.execute(f"UPDATE bots_games SET max_agr = max_agr + ? WHERE server_id_bg = ?", (5, interaction.user.guild.id,))
							else:
								pass

							if max_sen2 <= 50:
								emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
							else:
								tr1 = random.randint(1, 2)
								if tr1 == 1:
									cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif tr1 == 2:
									cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))

								r1 = random.randint(1, 8)
								print("действия:", r1)
								if r1 == 1: #нечего.
									emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
									cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
									cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 2: #звуки RANDOM
									song_gh = cursor.execute(f"SELECT song FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if song_gh == 1:
										emb = discord.Embed( title =f"Вы услышали звуки скрежета!!", colour = discord.Color.blurple() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (2, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 3: #предметы RANDOM
									item_gh = cursor.execute(f"SELECT item_home FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if item_gh == 1:
										emb = discord.Embed( title =f"Упали книги!!", colour = discord.Color.blurple() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (3, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 4: #Эл.Предметы RANDOM
									el_item_gh = cursor.execute(f"SELECT el_item_home FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if el_item_gh == 1:
										emb = discord.Embed( title =f"Заиграло радио!!", colour = discord.Color.blurple() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (3, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 5: #Датчик движения
									move_gh = cursor.execute(f"SELECT sen1_item FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if move_gh == 1:
										sen1 = cursor.execute(f"SELECT sen1_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
										if sen1 == 1:
											emb = discord.Embed( title =f"Датчик движения зафиксировал призрака!!", colour = discord.Color.blurple() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (2, interaction.user.guild.id,))
										else:
											emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
											cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 6: #Камера
									camera_gh = cursor.execute(f"SELECT camera_item FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if camera_gh == 1:
										camera_g = cursor.execute(f"SELECT camera_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
										if camera_g == 1:
											emb = discord.Embed( title =f"На камерах был замечен огонек!!", colour = discord.Color.blurple() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (2, interaction.user.guild.id,))
										else:
											emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
											cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 7: #Книга
									item1_gh = cursor.execute(f"SELECT item1_home FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if item1_gh == 1:
										item1 = cursor.execute(f"SELECT item1_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
										if item1 == 1:
											item1_r = random.randint(1,5)
											if item1_r == 1:
												emb = discord.Embed( title =f"В книге было написано: Умри, Умри, Умри, Умри, Умри, Умри, Умри!!", colour = discord.Color.blurple() )
												cursor.execute(f"UPDATE bots_games SET agr = agr + ? WHERE server_id_bg = ?", (30, interaction.user.guild.id,))
												cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_ran, interaction.user.guild.id,))
											elif item1_r == 2:
												emb = discord.Embed( title =f"В книге было написано: Я вижу тебя!!", colour = discord.Color.blurple() )
												cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_ran, interaction.user.guild.id,))
											elif item1_r == 3:
												emb = discord.Embed( title =f"В книге было написано: Я убью тебя!!", colour = discord.Color.blurple() )
												cursor.execute(f"UPDATE bots_games SET agr = agr + ? WHERE server_id_bg = ?", (30, interaction.user.guild.id,))
												cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_ran, interaction.user.guild.id,))
											elif item1_r == 4:
												emb = discord.Embed( title =f"В книге было написано: Поиграй со мной!!", colour = discord.Color.blurple() )
												cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_ran, interaction.user.guild.id,))
											elif item1_r == 5:
												emb = discord.Embed( title =f"Я иду за тобой!!", colour = discord.Color.blurple() )
												cursor.execute(f"UPDATE bots_games SET agr = agr + ? WHERE server_id_bg = ?", (90, interaction.user.guild.id,))
												cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (sen2_nz, interaction.user.guild.id,))
										else:
											emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
											cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
								elif r1 == 8: #ДА/НЕТ
									item2_gh = cursor.execute(f"SELECT item2_home FROM ghosts WHERE ghost_id = ?", (ghost1,)).fetchone()[0]
									if item2_gh == 1:
										item2 = cursor.execute(f"SELECT item2_g FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]						
										if item2 == 1:
											emb = discord.Embed( title =f"Карандаш повернулся на (Да/Нет)!!", colour = discord.Color.blurple() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (2, interaction.user.guild.id,))
										else:
											emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
											cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
											cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))
									else:
										emb = discord.Embed( title =f"Нечего не произошло!!", colour = discord.Color.magenta() )
										cursor.execute(f"UPDATE bots_games SET sen2_g = ? WHERE server_id_bg = ?", (1, interaction.user.guild.id,))
										cursor.execute(f"UPDATE bots_games SET torch_g = ? WHERE server_id_bg = ?", (0, interaction.user.guild.id,))

							cursor.execute(f"UPDATE bots_games SET agr = agr + ? WHERE server_id_bg = ?", (5, interaction.user.guild.id,))
							cursor.execute(f"UPDATE bots_games SET level = level + ? WHERE server_id_bg =?", (1, interaction.user.guild.id,))
					cursor.execute(f"UPDATE users SET use_one = ? WHERE server_id = ?", (0, interaction.user.guild.id,))
					await interaction.channel.send( embed = emb )
					db.commit()
		finally:
			cursor.close()
			db.close()



async def setup(bot):
	await bot.add_cog(end_games(bot))