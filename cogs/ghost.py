import discord
from discord.ext import commands
from discord.ui import Select, View
from discord.ext.commands import bot
from discord import app_commands, SelectOption


class Select(discord.ui.Select):
	def __init__(self):
		options=[
			discord.SelectOption(label="Полтергейст", value="1", emoji="🎃"),
			discord.SelectOption(label="Демон", value="2", emoji="🎃"),
			discord.SelectOption(label="Тень", value="3", emoji="🎃"),
			discord.SelectOption(label="Мимик", value="4", emoji="🎃"),
			discord.SelectOption(label="Дух", value="5", emoji="🎃"),	
		]
		super().__init__(placeholder="Список", max_values=1, min_values=1, options=options)

	async def callback(self, interaction: discord.Interaction):
		if self.values[0] == "1":
			emb = discord.Embed(title="Полтергейст", description='- Звуки.\n- Взаимодейтвсие с мебелью.\n- Рейагирует Датчик движение.\n- Можно найти следы УФ-Фонариком.\n- Пишет в Книгу\n- поварачивает карандаш (Да/Нет)', colour = discord.Color.og_blurple())

		elif self.values[0] == "2":
			emb = discord.Embed(title="Демон", description='- Звуки.\n- Взаимодействие с Элетренной мебелью.\n- Можно найти следы УФ-Фонариком\n- Огонёк в камерах.', colour = discord.Color.og_blurple())

		elif self.values[0] == "3":
			emb = discord.Embed(title="Тень", description='- Звуки\n- Взаимодейтвсие с мебелью.\n- Взаимодействие с Элетренной мебелью.\n- Рейагирует Датчик движение.\n- ЭМП Уровень 5.\n- Пишет в Книгу', colour = discord.Color.og_blurple())

		elif self.values[0] == "4":
			emb = discord.Embed(title="Мимик", description='- Взаимодейтвсие с мебелью.\n- Взаимодействие с Элетренной мебелью.\n- Рейагирует Датчик движение.\n- ЭМП Уровень 5.\n- Можно найти следы УФ-Фонариком\n- Огонёк в камерах.\n- Пишет в Книгу\n- поварачивает карандаш (Да/Нет)', colour = discord.Color.og_blurple())

		elif self.values[0] == "5":
			emb = discord.Embed(title="Дух", description='- Звуки.\n- Взаимодейтвсие с мебелью.\n- ЭМП Уровень 5.\n- Пишет в Книгу.\n- поварачивает карандаш (Да/Нет)', colour = discord.Color.og_blurple())


		await interaction.response.edit_message( embed = emb )


class SelectView(discord.ui.View):
	def __init__(self, *, timeout=30):
		super().__init__(timeout=timeout)
		self.add_item(Select())

class ghost_games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name = "ghost", description="Поставить предмет")
	async def _ghost(self, interaction: discord.Interaction):
		await interaction.response.send_message("Список призраков", view=SelectView(), ephemeral=True)


async def setup(bot):
	await bot.add_cog(ghost_games(bot))