import asyncio

from discord import Intents
from discord.ext import commands

from baxxter.config import BOT_TOKEN

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command(name="reload")
async def reload(ctx):
    await ctx.send("Reloading cogs.music...")
    await bot.reload_extension("cogs.music")


asyncio.run(bot.load_extension("cogs.music"))

bot.run(BOT_TOKEN)
