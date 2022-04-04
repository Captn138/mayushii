from ast import IsNot
import discord, datetime, itertools, os, dotenv
from discord.ext import tasks, commands
from cogs.admin import Admin
from meta import MetaInfo as MI

client = commands.Bot('.')


class BotBasics:

    current_status = ''
    status = itertools.cycle(['with Okarin', 'GUILDS', 'UPTIME', f"in ver {MI.get_bot_version()}"])
    start_time = datetime.datetime.utcnow()

    def uptime():
        now = datetime.datetime.utcnow()
        delta = now-__class__.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds."

    @tasks.loop(seconds = 10)
    async def change_status():
        __class__.current_status = next(__class__.status)
        if __class__.current_status == 'UPTIME':
            status_text = f"since {__class__.uptime()}"
        elif __class__.current_status == 'GUILDS':
            status_text = f"in {len(client.guilds)} servers"
        else:
            status_text = __class__.current_status
        await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = status_text))

    def load_all():
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension[:-3]}")
        print("Loaded all extensions")

    def unload_all():
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension[:-3]}")
        print("Unloaded all extensions")


class ManagementCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @client.command()
    async def reload(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()):
                client.reload_extension(f"cogs.{extension}")
                print(f"Reloaded {extension}.py")
            else:
                BotBasics.unload_all()
                BotBasics.load_all()

    @client.command()
    async def load(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension}")
                print(f"Loaded {extension}.py")
            else:
                BotBasics.load_all()

    @client.command()
    async def unload(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.owner_id and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension}")
                print(f"Unloaded {extension}.py")
            else:
                BotBasics.unload_all()

    @client.command(aliases = ['oof'])
    async def off(ctx):
        if await client.is_owner(ctx.message.author):
            print("Shutting down...")
            await client.close()


@client.event
async def on_ready():
    print(f"{client.user.name} (id: {client.user.id}) logged in !")
    BotBasics.change_status.start()

def main():
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.remove_command('help')
    BotBasics.load_all()
    client.run(TOKEN)

if __name__ == "__main__":
    main()