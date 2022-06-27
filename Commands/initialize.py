import discord
from discord.ext import commands

class Initialize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Check the respond time of the bot', description='A simple command to check how much time the bot takes to respond a message') #commands
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(brief='A comfy hello', description='A command that returns a hello with the name of the user')
    async def hello(self, ctx):
        if ctx.author.id == 183405695066963968 or ctx.author.id == ctx.guild.owner_id:
            await ctx.send("Hello, master!")
        else: 

            await ctx.send('Hello, ' + ctx.author.name + '!')
    
def setup(bot):
    bot.add_cog(Initialize(bot))