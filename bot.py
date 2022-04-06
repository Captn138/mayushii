import discord, datetime, itertools, os, dotenv, logging
from discord.ext import tasks, commands
from meta import MetaInfo as MI

client = commands.Bot('.')


class BotBasics:

    def deltatime(start_time: datetime.datetime):
        now = datetime.datetime.utcnow()
        if start_time is None:
            return 0, 0, 0, 0
        delta = now-start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    def load_all():
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension[:-3]}")
        logging.info("Loaded all extensions")

    def unload_all():
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension[:-3]}")
        logging.info("Unloaded all extensions")


class ManagementCommands(commands.Cog):

    current_status = ''
    status = itertools.cycle(['with Okarin', 'GUILDS', 'UPTIME', f"in ver {MI.get_bot_version()}"])
    start_time = datetime.datetime.utcnow()

    def __init__(self, client):
        self.client = client

    @client.command()
    async def reload(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()):
                client.reload_extension(f"cogs.{extension}")
                logging.info(f"Reloaded {extension}.py")
            else:
                BotBasics.unload_all()
                BotBasics.load_all()

    @client.command()
    async def load(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension}")
                logging.info(f"Loaded {extension}.py")
            else:
                BotBasics.load_all()

    @client.command()
    async def unload(ctx, extension = None):
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.owner_id and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension}")
                logging.info(f"Unloaded {extension}.py")
            else:
                BotBasics.unload_all()

    @client.command(aliases = ['oof'])
    async def off(ctx):
        if await client.is_owner(ctx.message.author):
            logging.info("Shutting down...")
            await client.close()

    @tasks.loop(seconds = 10)
    async def change_status():
        __class__.current_status = next(__class__.status)
        if __class__.current_status == 'UPTIME':
            days, hours, minutes, seconds = BotBasics.deltatime(__class__.start_time)
            status_text = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds."
        elif __class__.current_status == 'GUILDS':
            status_text = f"in {len(client.guilds)} servers"
        else:
            status_text = __class__.current_status
        await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = status_text))


@client.event
async def on_ready():
    BotBasics.load_all()
    logging.info(f"{client.user.name} (id: {client.user.id}) logged in !")
    ManagementCommands.change_status.start()

def main():
    logging.basicConfig(filename='bot.log', filemode='w', level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.remove_command('help')
    client.run(TOKEN)

if __name__ == "__main__":
    main()