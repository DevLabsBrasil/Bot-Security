""" Código Fonte do bot da DevLabsBrasil 

__author__ = "Snarloff"
__version__ = "2.0"

"""

import discord

from discord.ext.commands import Bot
from discord.ext import commands, tasks
from os import listdir, environ, getenv
from pathlib import Path
from time import sleep
from itertools import cycle
from random import choice

def get_prefix():
	return ["dl.", "dl!"]

class DevLabs(Bot):
	def __init__(self):
		super().__init__(
			command_prefix=commands.when_mentioned_or(*get_prefix()),
			description="A DevLabs é uma comunidade que tem como intuito ajudar aqueles que querem se tornar um programador! E claro, aqueles que possui alguma dúvida ou erros nos códigos! #PartiuCodar")
		self.remove_command("help")
		self.status = [
			"#PartiuCodar", "Compartilhe com seus amigos nossa comunidade!", "discord.gg/Jft2wMS"]

	def load(self):
		for file in listdir("cogs/"):
			if not file.endswith(".py"):
				continue
			f = file.replace(".py", "")
			try:
				self.load_extension("cogs.%s" % f)
			except Exception as error:
				print("Erro: %s\nMódulo: %s" % (error,str(f.title())))
			else:
				print("%s foi carregado com sucesso!" % str(f.title()))

	@property
	def init(self):
		from dotenv import load_dotenv

		if not getenv("TOKEN"):
			load_dotenv(dotenv_path=Path(".env"))
		return self.run(getenv("TOKEN"))

	async def on_ready(self):
		print("> Bot Iniciado com Sucesso!")


bot = DevLabs()
bot.load()
statuses = bot.status

@tasks.loop(seconds=60, reconnect=True)
async def change_stt():
	stt = next(bot.statuses)
	await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=stt))

@change_stt.before_loop
async def wait_for_bot():

	await bot.wait_until_ready()
	bot.statuses = cycle(statuses)

if __name__ == '__main__':
	change_stt.start()
	bot.init()
