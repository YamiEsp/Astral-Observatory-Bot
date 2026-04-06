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

import logging

#Logs configs

logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a'),
            logging.StreamHandler()
        ]
)

logger = logging.getLogger('discord_bot')

#load Enviroment variables
load_dotenv()
Token = os.getenv('TOKEN')
IdASC = os.getenv('ASC_USER_ID')
IdAPS = os.getenv('APS_USER_ID')

#Gets prefix for the server
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix= get_prefix, intents = intents)

#Error Handler
@client.event
async def on_command_error(ctx, error):
        logger.error(error)
        match error:
            case commands.CommandNotFound:
                await ctx.send('Command not found')
            case commands.MissingPermissions:
                await ctx.send('You do not have permission to use that command')
            case commands.BotMissingPermissions:
                await ctx.send('Bot does not have permission to use this command')
            case commands.MissingRequiredArgument:
                await ctx.send('Missing arguments')
            case commands.CheckFailure:
                await ctx.send('Check Failure')
            case commands.BadArgument:
                await ctx.send('Invalid arguments')
            case commands.CommandOnCooldown:
                await ctx.send('Command on cooldown')
            case commands.CommandInvokeError:
                await ctx.send('Command InvokeError')
            case commands.NoPrivateMessage:
                await ctx.send('This command cannot be used in private messages')
            case commands.NotOwner:
                await ctx.send('You do not have permission to use this command')
            case commands.CommandError:
                await ctx.send('Command Error')


#On startup, this is the first code to run
@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')
    logger.info('Buscando prefixes.json')
    try:
        with open("prefixes.json", "r") as f:
            content = f.read()
        logger.info('prefixes.json encontrado')
    except FileNotFoundError:
        logger.warning('prefixes.json no encontrado, creando...')
        with open("prefixes.json", "w") as f:
            f.write("")
        logger.info('prefixes.json creado.')
    #search and load all cogs
    for filename in os.listdir('./Commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'Commands.{filename[:-3]}')
            logger.info(f'{filename[:-3]} has been loaded')

#Prefix Setter and getters (for the bot)
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '*'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#Deletion of the Prefix on server leave
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#Change of prefix for the server
@client.command()
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix set to {prefix}')

#Verification of ownership and auth
def is_owner(ctx):
    return ctx.author.id in [IdASC, IdAPS]

#load a new cog
@client.command(brief='"cog name": to load a new cog', describe='Load a new cog', aliases=['Load'])
@commands.check(is_owner)
async def load(ctx, extension):
    await client.load_extension(f'Commands.{extension}')
    logger.info(f'{extension} has been loaded')
    await ctx.send(f'Loaded {extension}')

#unload a cog 
@client.command(brief='"cog name": to unload a cog', describe='Unload a cog', aliases=['Unload'])
@commands.check(is_owner)
async def unload(ctx, extension):
    await client.unload_extension(f'Commands.{extension}')
    logger.info(f'{extension} has been unloaded')
    await ctx.send(f'Unloaded {extension}')


#Reload a cog
@client.command(brief='"cog name": to reload a cog', describe='Reload a cog', aliases=['Reload'])
@commands.check(is_owner)
async def reload(ctx, extension):
    await client.reload_extension(f'Commands.{extension}')
    logger.info(f'{extension} has been reloaded')
    await ctx.send(f'Reloaded {extension}')


#List cogs
@client.command(brief='"list of all cogs', describe='list of cogs', aliases=['Lc', 'lc', 'LC', 'lC', 'cogs '])
@commands.check(is_owner)
async def list_cogs(ctx):
    loaded = list(client.extensions.keys())
    for filename in os.listdir('./Commands'):
        if filename.endswith('.py'):
            name = f'Commands.{filename[:-3]}'
            status = "🟢 Loaded" if name in loaded else "🔴 Not loaded"
            await ctx.send(f'{filename[:-3]} is present and (voting) {status}')
            logger.info(f'{filename[:-3]} is present and (voting) {status}')

client.run(Token)
