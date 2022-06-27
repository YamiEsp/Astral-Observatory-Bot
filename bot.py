from ast import alias
import os
from pydoc import describe
import json
from sys import prefix
from tokenize import Token
import discord
from discord.ext import commands

from dotenv import load_dotenv


load_dotenv()
Token = os.getenv('TOKEN')

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix= get_prefix)
 
@client.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing permissions')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('Bot missing permissions')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('Check failure')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Command on cooldown')
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send('Command invoke error')
        elif isinstance(error, commands.CommandError):
            await ctx.send('Command error')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Prefix Setter and reader (for the bot)
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '*'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
@client.command()
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix set to {prefix}')

#load a new cog
@client.command(brief='"cog name": to load a new cog', describe='Load a new cog', aliases=['Load'])
async def load(ctx, extension):
    client.load_extension(f'Commands.{extension}')
    print (f'{extension} has been loaded')
    await ctx.send(f'Loaded {extension}')

#unload a cog 
@client.command(brief='"cog name": to unload a cog', describe='Unload a cog', aliases=['Unload'])
async def unload(ctx, extension):
    client.unload_extension(f'Commands.{extension}')
    print (f'{extension} has been unloaded')
    await ctx.send(f'Unloaded {extension}')

#Reload a cog
@client.command(brief='"cog name": to reload a cog', describe='Reload a cog', aliases=['Reload'])
async def reload(ctx, extension):
    client.reload_extension(f'Commands.{extension}')
    print (f'{extension} has been reloaded')
    await ctx.send(f'Reloaded {extension}')

#search and load all cogs
for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        client.load_extension(f'Commands.{filename[:-3]}')
        print (f'{filename[:-3]} has been loaded')
    

client.run(Token)