import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands
import sqlite3
import random

class profile_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "profile", description="Посмотреть свой профиль или профиль другого игрока.!")
	async def _profile(self, interaction: discord.Interaction, member: discord.Member = None):
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			if member == None:
				win = cursor.execute(f"SELECT win_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
				lose = cursor.execute(f"SELECT lose_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
				money = cursor.execute(f"SELECT money_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
				rank_p = cursor.execute(f"SELECT rank_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
				online = cursor.execute(f"SELECT action_on_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
				if online == 1:
					online_p = "Не играет"
				elif online == 2:
					online_p = "В лобби"
				elif online == 3:
					online_p = "В игре"

				if rank_p == 9:
					rank_t = cursor.execute(f"SELECT name_rank FROM rank WHERE id_rank=?", (rank_p,)).fetchone()[0]
				else:
					rank_up = rank_p + 1
					rank_upt = cursor.execute(f"SELECT win_min FROM rank WHERE id_rank=?", (rank_up,)).fetchone()[0]
					if win >= rank_upt:
						cursor.execute(f"UPDATE profile SET rank_p = rank_p + ? WHERE id_p = ?", (1, interaction.user.id,))
						db.commit()
						rank_p = cursor.execute(f"SELECT rank_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
						rank_t = cursor.execute(f"SELECT name_rank FROM rank WHERE id_rank=?", (rank_p,)).fetchone()[0]
					else:
						rank_p = cursor.execute(f"SELECT rank_p FROM profile WHERE id_p=?", (interaction.user.id,)).fetchone()[0]
						rank_t = cursor.execute(f"SELECT name_rank FROM rank WHERE id_rank=?", (rank_p,)).fetchone()[0]



				emb = discord.Embed( title =f"Профиль",description = f'Онлайн - ***{online_p}*** \n \nРанг - ***{rank_t}***\nПобеды - ***{win}***\n Проигрыши - ***{lose}***\n Монеты - ***{money}***💵\n' ,colour = discord.Color.og_blurple() )
				emb.set_author(name = interaction.user.name, icon_url = interaction.user.avatar)
			else:
				win = cursor.execute(f"SELECT win_p FROM profile WHERE id_p=?", (member.id,)).fetchone()[0]
				lose = cursor.execute(f"SELECT lose_p FROM profile WHERE id_p=?", (member.id,)).fetchone()[0]
				money = cursor.execute(f"SELECT money_p FROM profile WHERE id_p=?", (member.id,)).fetchone()[0]
				rank_p = cursor.execute(f"SELECT rank_p FROM profile WHERE id_p=?", (member.id,)).fetchone()[0]
				online = cursor.execute(f"SELECT action_on_p FROM profile WHERE id_p=?", (member.id,)).fetchone()[0]
				if online == 1:
					online_p = "Не играет"
				elif online == 2:
					online_p = "В лобби"
				elif online == 3:
					online_p = "В игре"

				rank_t = cursor.execute(f"SELECT name_rank FROM rank WHERE id_rank=?", (rank_p,)).fetchone()[0]

				emb = discord.Embed( title =f"Профиль",description = f'Онлайн - ***{online_p}*** \n \nРанг - ***{rank_t}***\nПобеды - ***{win}***\n Проигрыши - ***{lose}***\n Монеты - ***{money}***💵\n' ,colour = discord.Color.og_blurple() )
				emb.set_author(name = member.name, icon_url = member.avatar)


			await interaction.response.send_message( embed = emb, ephemeral=True )

		finally:
			cursor.close()
			db.close()


async def setup(bot):
	await bot.add_cog(profile_games(bot))