"""Contain :class:`~admin.Admin: class, which contains admin commands definitions."""

import discord
import logging
from discord.ext import commands


class Admin(commands.Cog):
    """Contain administration commands."""

    def __init__(self, client):
        """Build the :class:`~admin.Admin` Class.

        Args:
            client (discord.ext.commands.bot): The bot on which to load the class.
        """
        self.client = client

    @commands.command(aliases=['c'])
    async def clear(self, ctx, amount: int = 1, userArg: discord.User = None):
        """Clear a number of messages.

        If no amount is specified, clears the last message. Can also specify a Discord User to filter on.

        Args:
            amount (int, optional): The amount of messages to delete. Defaults to 1.
            userArg (discord.User, optional): The user on which to filter. Defaults to None.
        """
        if ctx.message.author.guild_permissions.manage_messages is True:
            logging.info(f">>>Called command 'clear' with argument {amount} : {ctx.message.author}")
            if userArg is not None:
                logging.info(f" Targeted user: {userArg}")
                userid = str(userArg)[3:-1]
                await ctx.message.delete()
                async for message in ctx.channel.history(limit=500):
                    counter = 0
                    if int(message.author.id) == int(userid):
                        counter += 1
                        if counter <= amount+1:
                            await message.delete()
            else:
                await ctx.channel.purge(limit=amount+1)
            await ctx.send(f"I have deleted {amount} messages for ya!", delete_after=5)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kick a member from the server.

        Args:
            member (discord.Member): The member to kick.
            reason (str, optional): The reason of the kick. Defaults to None.
        """
        if ctx.message.author.guild_permissions.kick_members is True and member is not None:
            logging.info(f">>>Called command 'kick' of {member} with reason '{reason}' : {ctx.message.author}")
            await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Ban a member from the server.

        Args:
            member (discord.Member): The member to ban.
            reason (str, optional): The reason of the ban. Defaults to None.
        """
        if ctx.message.author.guild_permissions.ban_members is True and member is not None:
            logging.info(f">>>Called command 'ban' of {member} with reason '{reason}' : {ctx.message.author}")
            await member.ban(reason=reason)

    @commands.command()
    async def unban(self, ctx, *, member: str):
        """Unban a member from the server.

        Args:
            member (str): The username of the member to unban.
        """
        if ctx.message.author.guild_permissions.ban_members is True and member is not None:
            logging.info(f">>>Called command 'unban' of {member} : {ctx.message.author}")
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discirminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    return

    @commands.command(aliases=['arole'])
    async def autorole(self, ctx, var='True'):
        """Set up the automatic role when joining.

        Args:
            var (str, optional): The state to set. Defaults to 'True'.
        """
        if ctx.message.author.guild_permissions.manage_roles is True:
            logging.info(f">>>Called command 'autorole' on [{ctx.guild}] with argument {var} : {ctx.message.author}")
            data = []
            with open(f"./guilds/{ctx.guild.id}.guild", "r") as file:
                data = file.readlines()
            if var == 'False':
                with open(f"./guilds/{ctx.guild.id}.guild", "w") as file:
                    file.write(data[0])
                    file.write("False")
                await ctx.send("Autoroles have been disabled", delete_after=5)
            elif var == 'True':
                await ctx.send("Type the new autorole, or type 'cancel' to cancel the operation", delete_after=15)
                answer = await self.client.wait_for('message', timeout=15)
                if answer.content == 'cancel':
                    await ctx.send("Canceled!", delete_after=5)
                    await answer.delete()
                    return
                else:
                    with open(f"./guilds/{ctx.guild.id}.guild", "w") as file:
                        file.write(f"{answer.content}\nTrue")
                    await ctx.send(f"Autoroles have been changed to {answer.content}", delete_after=5)


async def setup(client):
    """Load the class on the bot.

    Args:
        client (discord.ext.commands.bot): The bot on which to load the class.
    """
    await client.add_cog(Admin(client))
