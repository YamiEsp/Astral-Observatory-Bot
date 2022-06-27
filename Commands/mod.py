import discord
from discord.ext import commands
import asyncio

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        async for message in ctx.channel.history(limit=amount + 1):
            await message.delete()
        await ctx.send(f'Cleared {amount} messages', delete_after=3)


    
def setup(bot):
    bot.add_cog(Mod(bot))