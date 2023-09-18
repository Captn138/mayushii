"""Main file for Mayushii, defines the body of the bot."""

import discord
import datetime
import itertools
import os
import dotenv
import logging
import sys
from discord.ext import tasks
from discord.ext import commands
from meta import MetaInfo


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s",
                    handlers=[logging.FileHandler(filename="bot.log", mode="a"), logging.StreamHandler(sys.stdout)])
current_status = ''
status = itertools.cycle(['with Okarin', 'GUILDS', 'UPTIME', f"in ver {MetaInfo.get_bot_version()}"])
start_time = datetime.datetime.utcnow()
cycle_time = 10
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')


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


async def load_all():
    """Load all modules located in ./cogs directory."""
    for extension in os.listdir('./cogs'):
        if extension.endswith('.py') and bot.get_cog(extension[:-3].capitalize()) is None:
            await bot.load_extension(f"cogs.{extension[:-3]}")
    logging.info("Loaded all extensions")


async def unload_all():
    """Unload all modules located in ./cogs directory."""
    for extension in os.listdir('./cogs'):
        if extension.endswith('.py') and bot.get_cog(extension[:-3].capitalize()):
            await bot.unload_extension(f"cogs.{extension[:-3]}")
    logging.info("Unloaded all extensions")


@bot.command()
async def reload(ctx, extension: str = None):
    """Reload a module located in ./cogs directory.

    Actually calls :func:`~bot.unload_all` and \
    :func:`~bot.unload_all` if no argument is passed.

    Args:
        extension (str, optional): The extension to reload. Defaults to None.
    """
    if await bot.is_owner(ctx.message.author):
        if extension is not None and bot.get_cog(extension[:-3].capitalize()):
            bot.reload_extension(f"cogs.{extension}")
            logging.info(f"Reloaded {extension}.py")
        else:
            await unload_all()
            await load_all()


@bot.command()
async def load(ctx, extension: str = None):
    """Load a module located in ./cogs directory. Actually calls :func:`~bot.load_all` if no argument is passed.

    Args:
        extension (str, optional): The extension to load. Defaults to None.
    """
    if await bot.is_owner(ctx.message.author):
        if extension is not None and bot.get_cog(extension[:-3].capitalize()) is None:
            bot.load_extension(f"cogs.{extension}")
            logging.info(f"Loaded {extension}.py")
        else:
            await load_all()


@bot.command()
async def unload(ctx, extension: str = None):
    """Unload a module located in ./cogs directory. Actually calls :func:`~bot.unload_all` if no argument is \
    passed.

    Args:
        extension (str, optional): The extension to unload. Defaults to None.
    """
    if await bot.is_owner(ctx.message.author):
        if extension is not None and bot.owner_id and bot.get_cog(extension[:-3].capitalize()):
            bot.unload_extension(f"cogs.{extension}")
            logging.info(f"Unloaded {extension}.py")
        else:
            await unload_all()


@bot.command(aliases=['oof'])
async def off(ctx, msg):  # TODO: trouver pourquoi il faut 2 arguments ici
    """Turn off the bot."""
    if await bot.is_owner(ctx.message.author):
        logging.info("Shutting down...")
        await bot.close()


@tasks.loop(seconds=cycle_time)
async def change_status():
    """Change the displayed status on a clock basis."""
    current_status = next(status)
    if current_status == 'UPTIME':
        days, hours, minutes, seconds = deltatime(start_time)
        status_text = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds."
    elif current_status == 'GUILDS':
        status_text = f"in {len(bot.guilds)} servers"
    else:
        status_text = current_status
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=status_text))


@bot.event
async def on_ready():
    """Log when the bot is ready."""
    await load_all()
    logging.info(f"{bot.user.name} (id: {bot.user.id}) logged in !")
    change_status.start()


def main():
    """Run the bot."""
    dotenv.load_dotenv()
    TOKEN = os.getenv('TOKEN')
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
