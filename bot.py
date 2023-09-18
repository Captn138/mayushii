"""Main file for Mayushii, defines the body of the bot."""

import discord
import datetime
import itertools
import os
import dotenv
import logging
from discord.ext import tasks
from discord.ext import commands
from meta import MetaInfo

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)


class BotBasics:
    """Provide load and unload functions, as well as a delta of time."""

    def deltatime(start_time: datetime.datetime):
        """Provide a time delta.

        Args:
            start_time (datetime.datetime): The time from which to compute the delta.

        Returns:
            (int, int, int, int): A tuple containing the delta in days, hours, minutes and seconds.
        """
        now = datetime.datetime.utcnow()
        if start_time is None:
            return 0, 0, 0, 0
        delta = now-start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    def load_all():
        """Load all modules located in ./cogs directory."""
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension[:-3]}")
        logging.info("Loaded all extensions")

    def unload_all():
        """Unload all modules located in ./cogs directory."""
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py') and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension[:-3]}")
        logging.info("Unloaded all extensions")


class ManagementCommands(commands.Cog):
    """Provide management commands that can be called from Discord, such as :func:`~bot.ManagementCommands.load`, \
    :func:`~bot.ManagementCommands.unload` and :func:`~bot.ManagementCommands.reload`."""

    def __init__(self, client: commands.bot):
        """Build the :class:`~bot.ManagementCommands` Class.

        Args:
            client (discord.ext.commands.bot): The bot on which to load the class.
        """
        self.client = client
        self.current_status = ''
        self.status = itertools.cycle(['with Okarin', 'GUILDS', 'UPTIME', f"in ver {MetaInfo.get_bot_version()}"])
        self.start_time = datetime.datetime.utcnow()
        self.cycle_time = 10

    @client.command()
    async def reload(ctx, extension: str = None):
        """Reload a module located in ./cogs directory.

        Actually calls :func:`~bot.BotBasics.unload_all` and \
        :func:`~bot.BotBasics.unload_all` if no argument is passed.

        Args:
            extension (str, optional): The extension to reload. Defaults to None.
        """
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()):
                client.reload_extension(f"cogs.{extension}")
                logging.info(f"Reloaded {extension}.py")
            else:
                BotBasics.unload_all()
                BotBasics.load_all()

    @client.command()
    async def load(ctx, extension: str = None):
        """Load a module located in ./cogs directory. Actually calls :func:`~bot.BotBasics.load_all` if no argument is passed.

        Args:
            extension (str, optional): The extension to load. Defaults to None.
        """
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.get_cog(extension[:-3].capitalize()) is None:
                client.load_extension(f"cogs.{extension}")
                logging.info(f"Loaded {extension}.py")
            else:
                BotBasics.load_all()

    @client.command()
    async def unload(ctx, extension: str = None):
        """Unload a module located in ./cogs directory. Actually calls :func:`~bot.BotBasics.unload_all` if no argument is \
        passed.

        Args:
            extension (str, optional): The extension to unload. Defaults to None.
        """
        if await client.is_owner(ctx.message.author):
            if extension is not None and client.owner_id and client.get_cog(extension[:-3].capitalize()):
                client.unload_extension(f"cogs.{extension}")
                logging.info(f"Unloaded {extension}.py")
            else:
                BotBasics.unload_all()

    @client.command(aliases=['oof'])
    async def off(ctx):
        """Turn off the bot."""
        if await client.is_owner(ctx.message.author):
            logging.info("Shutting down...")
            await client.close()

    @tasks.loop(seconds=__class__.cycle_time)
    async def change_status():
        """Change the displayed status on a clock basis."""
        __class__.current_status = next(__class__.status)
        if __class__.current_status == 'UPTIME':
            days, hours, minutes, seconds = BotBasics.deltatime(__class__.start_time)
            status_text = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds."
        elif __class__.current_status == 'GUILDS':
            status_text = f"in {len(client.guilds)} servers"
        else:
            status_text = __class__.current_status
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name=status_text))


@client.event
async def on_ready():
    """Log when the bot is ready."""
    BotBasics.load_all()
    logging.info(f"{client.user.name} (id: {client.user.id}) logged in !")
    ManagementCommands.change_status.start()


def main():
    """Load the environment variables and runs the bot."""
    logging.basicConfig(filename='bot.log', filemode='w', level=logging.INFO,
                        format="%(asctime)s - %(levelname)s: %(message)s")
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.remove_command('help')
    client.run(TOKEN)


if __name__ == "__main__":
    main()
