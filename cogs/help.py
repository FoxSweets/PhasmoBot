import discord
from discord.ext import commands
from discord.ui import Select, View
from discord.ext.commands import bot
from discord import app_commands

class Select(discord.ui.Select):
	def __init__(self):
		options=[
			discord.SelectOption(label="НАВИГАЦИЯ: команды до игры", value="1", emoji="📜", description="Команды которые вы можете использовать до игры!"),
			discord.SelectOption(label="НАВИГАЦИЯ: Команды во время игры", value="2", emoji="🔦", description="Команды которые вы можете использовать во время игры!"),
			discord.SelectOption(label="НАВИГАЦИЯ: Предметы", value="3", emoji="🛠", description="Придметы которые есть в игры, и вы их можете использовать!"),
			discord.SelectOption(label="НАВИГАЦИЯ: Призраки", value="4", emoji="🎃", description="Все призраки нашей игры!")
		]
		super().__init__(placeholder="Помощь", max_values=1, min_values=1, options=options)

	async def callback(self, interaction: discord.Interaction):
		if self.values[0] == "1":
			emb = discord.Embed(title="НАВИГАЦИЯ: команды до игры", description='`Join` - присоединиться к игре \n`leave` - Отключиться от игры \n`Start` - начать игру', colour = discord.Color.og_blurple() )
			await interaction.response.send_message( embed = emb, ephemeral=True )
		elif self.values[0] == "2":
			emb = discord.Embed(title="НАВИГАЦИЯ: Команды во время игры", description='`end` - закончить ход \n`use_item` - использовать предмет (1/2/3...) \n`inventory` - показывает предметы в инвентаре \n`ghost` - весь список призраков на сервере\n`theend` - закончить игру (1/2/3)', colour = discord.Color.og_blurple() )
			await interaction.response.send_message( embed = emb, ephemeral=True )
		elif self.values[0] == "3":
			emb = discord.Embed(title="НАВИГАЦИЯ: Предметы", description='1 - соль (спасает один раз) \n2 - крест (спасает один раз) \n3 - Датчик Движения \n4 - Датчик Активности Призрака \n5 - Камера \n6 - пустая книга \n7 - книга (Да/не) \n8 - УФ-Фонарик \n 9 - успокоение для призрака(понимажает минимум до нуля) \n 10 - шкатулка призрака(понимажает максимум на 20 единиц)', colour = discord.Color.og_blurple() )
			await interaction.response.send_message( embed = emb, ephemeral=True )
		elif self.values[0] == "4":
			emb = discord.Embed(title="НАВИГАЦИЯ: Призраки", description='1 - ***Полтергейст*** \n2 - ***Демон*** \n3 - ***Тень*** \n4 - ***Мимик***\n5 - ***Дух***\nузнать лучше можно командой `ghost`')
			await interaction.response.send_message( embed = emb, ephemeral=True )



class SelectView(discord.ui.View):
	def __init__(self, *, timeout=30):
		super().__init__(timeout=timeout)
		self.add_item(Select())


class help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "help", description="Помощь по командам бота!")
	async def _help(self, interaction: discord.Interaction):
		await interaction.response.send_message("Помощь по командам", view=SelectView(), ephemeral=True)

async def setup(bot):
	await bot.add_cog(help(bot))