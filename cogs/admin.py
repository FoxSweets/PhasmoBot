import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord import app_commands

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@app_commands.command(name="clear")
	@commands.is_owner()
	async def clear(self, interaction: discord.Interaction, limit: int = 1000):
		await interaction.response.send_message("сообщения удалены", ephemeral=True)
		await interaction.channel.purge( limit = limit )


async def setup(bot):
	await bot.add_cog(admin(bot))