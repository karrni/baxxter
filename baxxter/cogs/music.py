import discord
import yarl
import yt_dlp
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        channel = ctx.message.author.voice.channel
        voice_channel = await channel.connect()

        parsed_url = yarl.URL(url)
        domain = parsed_url.host

        supported_domains = (
            "www.youtube.com",
            "youtube.com",
            "soundcloud.com",
            "www.soundcloud.com",
        )

        if domain in supported_domains:
            ytdl_opts = {"format": "bestaudio"}

            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                info = ytdl.extract_info(url, download=False)
                audio_url = info["url"]
                voice_channel.play(
                    discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_url)
                )
        else:
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url))

    @commands.command()
    async def pause(self, ctx):
        await ctx.send("pause")

    @commands.command()
    async def resume(self, ctx):
        await ctx.send("resume")

    @commands.command()
    async def stop(self, ctx):
        await ctx.send("stop")


async def setup(bot):
    await bot.add_cog(Music(bot))
