#!/usr/bin/env python3
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
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix= get_prefix, intents = intents)

@client.event
async def on_command_error(ctx, error):
        print(error)
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
    #search and load all cogs
    for filename in os.listdir('./Commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'Commands.{filename[:-3]}')
            print (f'{filename[:-3]} has been loaded')

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
    if ctx.author.id == 183405695066963968 or ctx.author.id == 364077052795682816:
        client.load_extension(f'Commands.{extension}')
        print (f'{extension} has been loaded')
        await ctx.send(f'Loaded {extension}')
    else:
        await ctx.send('You do not have authorization')

#unload a cog 
@client.command(brief='"cog name": to unload a cog', describe='Unload a cog', aliases=['Unload'])
async def unload(ctx, extension):
    if ctx.author.id == 183405695066963968 or ctx.author.id == 364077052795682816:
        client.unload_extension(f'Commands.{extension}')
        print (f'{extension} has been unloaded')
        await ctx.send(f'Unloaded {extension}')
    else:
        await ctx.send('You do not have authorization')


#Reload a cog
@client.command(brief='"cog name": to reload a cog', describe='Reload a cog', aliases=['Reload'])
async def reload(ctx, extension):
    if ctx.author.id == 183405695066963968 or ctx.author.id == 364077052795682816:
        client.reload_extension(f'Commands.{extension}')
        print (f'{extension} has been reloaded')
        await ctx.send(f'Reloaded {extension}')
    else:
        await ctx.send('You do not have authorization')

#List cogs
@client.command(brief='"list of all cogs', describe='list of cogs', aliases=['List cogs', 'List Cogs', 'list cogs', 'list Cogs'])
async def list(ctx):
    if ctx.author.id == 183405695066963968 or ctx.author.id == 364077052795682816:
        for filename in os.listdir('./Commands'):
            if filename.endswith('.py'):
                await ctx.send(f'{filename[:-3]} is present and voting')
                print(f'{filename[:-3]} is present and voting')
    else:
        await ctx.send('You do not have authorization')
    

client.run(Token)