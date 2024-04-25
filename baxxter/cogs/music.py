import discord
import yarl
import yt_dlp
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        if not ctx.message.author.voice:
            await ctx.send("youre not in a voice channel my guy")
            return

        channel = ctx.message.author.voice.channel

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()

        ytdl_opts = {
            "format": "bestaudio/best",
            "extractaudio": True,
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "audioformat": "mp3",
            "noplaylist": True,
        }

        ffmpeg_opts = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            try:
                info = ytdl.extract_info(url, download=False)
                audio_url = info["url"]
                print(audio_url)
                voice_client.play(
                    discord.FFmpegPCMAudio(
                        executable="ffmpeg", source=audio_url, **ffmpeg_opts
                    )
                )

            except Exception as e:
                await ctx.send(f"error: {e}")
                return

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
