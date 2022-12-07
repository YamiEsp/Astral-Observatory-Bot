import discord
import typing
from discord.ext import commands
import wavelink

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.create_nodes())

    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="127.0.0.1", port="41727", password="testing")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")

    @commands.command(name="join", aliases=["connect", "summon"])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.send("bot is already connected to a voice channel")
        
        await channel.connect(cls=wavelink.Player)
        mbed=discord.Embed(title=f"Connected to {channel.name}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.command(name ="play", help = "Plays a song from YT", aliases=["p", "Play", "P"])
    async def play_command(self, ctx: commands.Context, *, search: str):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.play(search)

        mbed = discord.Embed(title=f"Now Playing {search}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)
        # if channel is None:
        #     channel = ctx.author.voice.channel
        
        # node = wavelink.NodePool.get_node()
        # player = node.get_player(ctx.guild)
        
        # await channel.connect(cls=wavelink.Player)
        # mbed=discord.Embed(title=f"Connected to {channel.name}", color=discord.Color.from_rgb(255, 255, 255))

        # search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        # if not ctx.voice.client:
        #     vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        # else:
        #     vc: wavelink.Pleyer = ctx.voice_client

        # await vc.play(search)

        # mbed = discord.Embed(title=f"Now Playing {search}", color = discord.Color.from_rgb(255, 255, 255))
        # await ctx.send(embed=mbed)

    @commands.command(name="stop")
    async def stop_command(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if player.is_playing:
            await player.stop()
            mbed = discord.Embed(title="Playback Stoped", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            return await ctx.send("Nothing Is playing right now")
    
    @commands.command(name="pause")
    async def pause_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                mbed = discord.Embed(title="Playback Paused", color=discord.Color.from_rgb(255, 255, 255))
                return await ctx.send(embed=mbed)
            else:
                return await ctx.send("Nothing is playing right now")
        else:
            return await ctx.send("Playback is Already paused")
    
    @commands.command(name="resume")
    async def resume_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("bot is not connnected to any voice channel")
        
        if player.is_paused():
            await player.resume()
            mbed = discord.Embed(title="Playback resumed", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            return await ctx.send("playback is not paused")

    @commands.command(name="volume")
    async def volume_command(self, ctx: commands.Context, to: int):
        if to > 100:
            return await ctx.send("Volume should be between 0 and 100")
        elif to < 1:
            return await ctx.send("Volume should be between 0 and 100")
        

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(to)
        mbed = discord.Embed(title=f"Changed Volume to {to}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)
    
    @commands.command(name="leave", help= "Disconnects the bot from the voice channel", aliases=["disconnect"])
    async def leave_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        await player.disconnect()
        mbed = discord.Embed(title="disconnected", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)
        
    
async def setup(bot):
    await bot.add_cog(Music(bot))