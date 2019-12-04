import discord
import datetime
import os
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

meta = open("meta.txt", "r").readlines()
status = cycle(['with Okarin', 'GUILDS', 'UPTIME', f'in ver {meta[0]}'])
start_time = datetime.datetime.utcnow()
uptime_stamp = ''
current_status = ''

def uptime():
    global uptime_stamp
    now = datetime.datetime.utcnow()
    delta = now-start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    time_format = "{d} days, {h} hours, {m} minutes, and {s} seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

@tasks.loop(seconds = 10)
async def change_status():
    uptime()
    global current_status
    current_status = next(status)
    if current_status == 'UPTIME':
        await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = f'since {uptime_stamp}'))
    elif current_status == 'GUILDS':
        await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = f'in {len(client.guilds)} guilds'))
    else:
        await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = current_status))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    change_status.start()

@client.command()
async def reload(ctx, extension = 'NULL'):
    if ctx.message.author.id == int(open("owner.txt", "r").readline(18)):
        if extension != 'NULL':
            client.unload_extension(f'cogs.{extension}')
            print(f"Unloaded {extension}.py")
            client.load_extension(f'cogs.{extension}')
            print(f"Loaded {extension}.py")
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
            print("Unloaded all extensions")
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.load_extension(f'cogs.{filename[:-3]}')
            print("Loaded all extensions")

@client.command()
async def load(ctx, extension = 'NULL'):
    if ctx.message.author.id == int(open("owner.txt", "r").readline(18)):
        if extension != 'NULL':
            client.load_extension(f'cogs.{extension}')
            print(f"Loaded {extension}.py")
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.load_extension(f'cogs.{filename[:-3]}')
            print("Loaded all extensions")

@client.command()
async def unload(ctx, extension = 'NULL'):
    if ctx.message.author.id == int(open("owner.txt", "r").readline(18)):
        if extension != 'NULL':
            client.unload_extension(f'cogs.{extension}')
            print(f"Unloaded {extension}.py")
        else:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
            print("Unloaded all extensions")

@client.command(aliases = ['oof'])
async def off(ctx):
    if ctx.message.author.id == int(open("owner.txt", "r").readline(18)):
        print("Shutting down...")
        await client.logout()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename}")

client.run(open("token.txt", "r").readline(59))