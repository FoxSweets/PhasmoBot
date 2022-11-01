import discord
from discord.ext import commands
from discord.ui import view
from discord.ext.commands import bot
from discord import app_commands
import sqlite3

class Buttons(discord.ui.View):
	def __init__(self, *, timeout = 180):
		super().__init__(timeout=timeout)


	@discord.ui.button(label="Да", style=discord.ButtonStyle.red)
	async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
		for child in self.children:
			child.disabled=True
		db = sqlite3.connect("./database.db")
		cursor = db.cursor()
		try:
			game4 = cursor.execute(f"SELECT players FROM bots_games").fetchone()[0]
			cursor.execute(f"SELECT id FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,))
			if cursor.fetchone() is None:
				emb = discord.Embed( title =f"Сперва зайдите в игру!!", colour = discord.Color.red() )
				await interaction.response.edit_message( embed = emb, view=self)
			else:
				game = cursor.execute(f"SELECT activ_game FROM users WHERE id=? AND server_id = ?", (interaction.user.id, interaction.user.guild.id,)).fetchone()[0]
				if game == 0:
					emb = discord.Embed( title =f"Сперва зайдите в игру!!", colour = discord.Color.red() )
					await interaction.response.edit_message( embed = emb, view=self)
				elif game == 1:
					cursor.execute(f"UPDATE profile SET action_on_p = ? WHERE id_p = ?", (1, interaction.user.id,))
					cursor.execute(f"UPDATE profile SET server_id_p = ? WHERE id_p = ?", (0, interaction.user.id,))
					cursor.execute(f"UPDATE bots_games SET players = players - 1 WHERE server_id_bg = ?", (interaction.user.guild.id,))
					cursor.execute(f"UPDATE users SET activ_game = ? WHERE id = ? AND server_id = ?", (0, interaction.user.id, interaction.user.guild.id,))
					cursor.execute(f"UPDATE users SET player = ? WHERE id = ? AND server_id = ?", (0, interaction.user.id, interaction.user.guild.id,))
					game4 = cursor.execute(f"SELECT players FROM bots_games WHERE server_id_bg = ?", (interaction.user.guild.id,)).fetchone()[0]
					
					emb = discord.Embed( title =f"вы отключился от игре!!", colour = discord.Color.green() )
					await interaction.response.edit_message( embed = emb, view=self)

					emb = discord.Embed( title =f"{interaction.user.name} отключился от игре!! ({game4}/4)", colour = discord.Color.red() )
					await interaction.channel.send( embed = emb )
			db.commit()
		finally:
			cursor.close()
			db.close()

	@discord.ui.button(label="Нет", style=discord.ButtonStyle.green)
	async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
		for child in self.children:
			child.disabled=True
		emb = discord.Embed( title =f"Вы остались в лобби!", colour = discord.Color.green() )
		await interaction.response.edit_message( embed = emb, view=self)


class leave_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@app_commands.command(name = "leave", description="выйти из игры")
	async def _leave(self, interaction: discord.Interaction):
		emb = discord.Embed( title =f"Вы точно хотите выйти с лобби?", colour = discord.Color.gold() )
		await interaction.response.send_message(embed=emb, view=Buttons(), ephemeral=True )


async def setup(bot):
	await bot.add_cog(leave_games(bot))