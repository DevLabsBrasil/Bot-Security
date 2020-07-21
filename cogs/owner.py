import discord
import time, datetime, psutil, platform
from discord.ext.commands import *
from random import randint

class Owner(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.start_time = time.time()
		self.color = 0x646ecb

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command(aliases=["upt"])
	async def uptime(self, ctx):
		current_time = time.time()
		difference = int(round(current_time - self.start_time))
		text = str(datetime.timedelta(seconds=difference))

		return await ctx.send(embed=discord.Embed(color=self.color,description="Estou online à %ss" %(text)))

	@cooldown(2, 10, BucketType.user)
	@guild_only()
	@command()
	async def botinfo(self, ctx):
		embed = discord.Embed(color=self.color, timestamp = ctx.message.created_at)

		embed.description = (
			"**DevLabs**\n\n"
			"**ID:** %s\n"
			"**Ping:** %sms\n"
			"**CPU:** %s\n"
			"**Memory:** %s\n"
			"**System:** %s\n"
			"**Release:** %s\n"
			"**Uptime:** %s"
			%(ctx.me.id, round(self.bot.latency*1000),
			str(psutil.cpu_percent()) + "%", str(psutil.virtual_memory().percent) + "%",
			platform.system(), platform.release(),
			str(datetime.timedelta(seconds=int(round(time.time() - self.start_time))))))
		return await ctx.send(embed=embed)

	@guild_only()
	@command(aliases=["rld"])
	@is_owner()
	async def reload(self, ctx, ext:str=None):
		try:
			self.bot.unload_extension("cogs.%s" %(ext))
			self.bot.load_extension("cogs.%s" %(ext))
		except Exception as error:
			return await ctx.send(embed=discord.Embed(color=self.color, description="Falha ao recarregar o módulo %s.\nErro: %s" %(ext, error)))
		else:
			return await ctx.send(embed=discord.Embed(color=self.color, description="O módulo %s foi recarregado." %(ext)))

	@guild_only()
	@command(aliases=["uld"])
	@is_owner()
	async def unload(self, ctx, ext:str=None):	
		try:
			self.bot.unload_extension("cogs.%s" %(ext))
		except Exception as error:
			return await ctx.send(embed=discord.Embed(color=self.color, description="Falha ao descarregar o módulo %s.\nErro: %s" %(ext, error)))
		else:
			return await ctx.send(embed=discord.Embed(color=self.color, description="O módulo %s foi descarregado." %(ext)))

	@guild_only()
	@command(aliases=["lda"])
	@is_owner()
	async def load(self, ctx, ext:str=None):	
		try:
			self.bot.load_extension("cogs.%s" %(ext))
		except Exception as error:
			return await ctx.send(embed=discord.Embed(color=self.color, description="Falha ao carregar o módulo %s.\nErro: %s" %(ext, error)))
		else:
			return await ctx.send(embed=discord.Embed(color=self.color, description="O módulo %s foi carregado." %(ext)))		

	@is_owner()
	@command(aliases=["evap", "debugger", "debug"])
	async def eval(self, ctx, *, cmd=None):
		f = discord.Embed(color=self.color, description=f"**Console DevLabs**")
		try:
			if "bot." in cmd:
				Debugger = (eval(cmd.replace("bot.", "self.bot.")))
				f.add_field(name="Input:", value=f"```py\n{cmd}```")
				f.add_field(name="Output:", value=f"```py\n{Debugger}```")
				await ctx.send(embed=f)
			elif "await " in cmd:
				Debugger = (await eval(cmd.replace("await ", "")))
				f.add_field(name="Input:", value=f"```py\n{cmd}```")
				f.add_field(name="Output:", value=f"```py\n{Debugger}```")
				await ctx.send(embed=f)
			else:
				Debugger = (eval(cmd))
				f.add_field(name="Input:", value=f"```py\n{cmd}```")
				f.add_field(name="Output:", value=f"```py\n{Debugger}```")
				await ctx.send(embed=f)				
		except Exception as e:
			f = discord.Embed(color=ctx.author.color, description=f"**Console Developer's Brasil**")
			f.add_field(name="Input:", value=f"```py\n{cmd}```")
			f.add_field(name="Output:", value=f"```py\n{repr(e)}```")
			await ctx.send(embed=f)
		except discord.HTTPException:
			f.add_field(name="Input:", value=f"```py\n{cmd}```")
			f.add_field(name="Output:", value=f"```py\n{repr()}```")

def setup(bot):
	bot.add_cog(Owner(bot))