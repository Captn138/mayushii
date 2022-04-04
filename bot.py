import discord, datetime, itertools, os, dotenv
from discord.ext import tasks, commands
from meta import MetaInfo as MI

current_status = ''
status = itertools.cycle(['with Okarin', 'GUILDS', 'UPTIME', f"in ver {MI.get_bot_version()}"])
start_time = datetime.datetime.utcnow()

client = commands.Bot('.')

def uptime():
    now = datetime.datetime.utcnow()
    delta = now-start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    return f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds."

@tasks.loop(seconds = 10)
async def change_status():
    global current_status
    current_status = next(status)
    if current_status == 'UPTIME':
        status_text = f"since {uptime()}"
    elif current_status == 'GUILDS':
        status_text = f"in {len(client.guilds)} servers"
    else:
        status_text = current_status
    await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = status_text))

@client.event
async def on_ready():
    print(f"{client.user.name} (id: {client.user.id}) logged in !")
    change_status.start()

def load_all():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
    print("Loaded all extensions")

def unload_all():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f"cogs.{filename[:-3]}")
    print("Unloaded all extensions")

@client.command()
async def reload(ctx, extension = None):
    if ctx.message.author.id == MI.get_author_id():
        if extension != None:
            client.unload_extension(f"cogs.{extension}")
            print(f"Unloaded {extension}.py")
            client.load_extension(f"cogs.{extension}")
            print(f"Loaded {extension}.py")
        else:
            unload_all()
            load_all()

@client.command()
async def load(ctx, extension = None):
    if ctx.message.author.id == MI.get_author_id():
        if extension != None:
            client.load_extension(f"cogs.{extension}")
            print(f"Loaded {extension}.py")
        else:
            load_all()

@client.command()
async def unload(ctx, extension = None):
    if ctx.message.author.id == MI.get_author_id():
        if extension != None:
            client.unload_extension(f"cogs.{extension}")
            print(f"Unloaded {extension}.py")
        else:
            unload_all()

@client.command(aliases = ['oof'])
async def off(ctx):
    if ctx.message.author.id == MI.get_author_id():
        print("Shutting down...")
        await client.close()

def main():
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.remove_command('help')
    load_all()
    client.run(TOKEN)

if __name__ == "__main__":
    main()