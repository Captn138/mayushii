"""Contain :class:`~events.Events: class, which contains event triggers definitions."""

import discord
import os
import logging
from discord.ext import commands


class Events(commands.Cog):
    """Contain event triggers."""

    def __init__(self, client):
        """Build the :class:`~admin.Admin` Class.

        Args:
            client (discord.ext.commands.bot): The bot on which to load the class.
        """
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.User):
        """Trigger on member join.

        Args:
            member (discord.User): The user that joined.
        """
        if member.bot is False:
            logging.info(f'>>>>>[{member.guild}] New member: {member}')
            data = []
            for filename in os.listdir('./guilds'):
                if filename == f'{member.guild.id}.guild':
                    with open(f'./guilds/{filename}', 'r') as file:
                        data = file.readlines()
            if data[1] == 'True':
                role = discord.utils.get(member.guild.roles, name=data[0][:-1])
                await member.add_roles(role)
        else:
            logging.info(f'>>>>>[{member.guild}] New bot: {member}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Trigger when joining a server.

        Args:
            guild (discord.Guild): The server that has been joined.
        """
        with open(f"./guilds/{guild.id}.guild", "w+") as file:
            file.write("\nFalse")
        await guild.owner.send(f"Tuturuuu! I'm {self.client.user.name}! Thanks for adding me to your \
            guild! My prefix is **{self.client.get_prefix()}**. Don't forget to place my role on top of all the \
                others so I can work properly.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: discord.ext.commands.CommandError):
        """Trigger on command errors.

        Args:
            error : The error raised.
        """
        passerrors = (commands.CommandNotFound, commands.MissingRequiredArgument)
        if isinstance(error, passerrors):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            logging.error(f"Exception on command '{ctx.message.content}':\n\t{error}")


async def setup(client):
    """Load the class on the bot.

    Args:
        client (discord.ext.commands.bot): The bot on which to load the class.
    """
    await client.add_cog(Events(client))
