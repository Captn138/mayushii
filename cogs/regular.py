"""Contain :class:`~regular.Regular: class, which contains regular commands definitions."""

import discord
import asyncio
import datetime
import logging
from discord.ext import commands
from meta import MetaInfo
from bot import deltatime


class Regular(commands.Cog):
    """Contain regular commands."""

    def __init__(self, client):
        """Build the :class:`~admin.Admin` Class.

        Args:
            client (discord.ext.commands.bot): The bot on which to load the class.
        """
        self.client = client
        self.last_youy: datetime.datetime = None
        self.youy_limit = 5

    @commands.command(aliases=['t'])
    async def tuturu(self, ctx):
        """Connect to voice chat to sing 'Tuturu'."""
        logging.info(">>>Called command 'tuturu'")
        destination = ctx.message.author.voice.channel
        vc = await destination.connect()
        vc.play(discord.FFmpegPCMAudio('tuturu.mp3'))
        await asyncio.sleep(2)
        await vc.disconnect()

    @commands.command()
    async def youy(self, ctx):
        """Send the youy in chat."""
        logging.info(">>>Called command 'youy'")
        days, hours, minutes, seconds = deltatime(__class__.last_youy)
        if __class__.last_youy is None or (days*24*60)+(hours*60)+minutes > __class__.youy_limit:
            __class__.last_youy = datetime.datetime.utcnow()
            await ctx.send
            ("https://media.discordapp.net/attachments/622011856642637825/622012196397776896/JPEG_20181001_113150.jpg")
        else:
            await ctx.send(f"Holà vilain garnement! Tu dois attendre {__class__.youy_limit} minutes entre chaque youy.")

    @commands.command()
    async def invite(self, ctx):
        """Send the invite link in chat."""
        logging.info(">>>Called command 'invite'")
        await ctx.message.delete()
        bot_message = await ctx.send(f"Here's an invite link to my creator's server! Link will be removed in 15 seconds: \
            {MetaInfo.get_owner_server_invite_link()}")
        await bot_message.delete(delay=15)

    @commands.command()
    async def ping(self, ctx):
        """Send the latency in chat."""
        logging.info(">>>Called command 'ping'")
        await ctx.send(f'Pong! [{round(self.client.latency*1000)}ms]', delete_after=3)
        await ctx.message.delete(delay=3)

    @commands.command()
    async def dev(self, ctx):
        """Send the dev history in chat."""
        logging.info(">>>Called command 'dev'")
        embed = discord.Embed(title=f"{self.client.user.name}'s dev history", description="All my updates should be here.",
                              color=0xa1ee33)
        embed.set_thumbnail(url=MetaInfo.get_embed_thumbnail_url())
        embed.add_field(inline=False, name="Source code", value="https://github.com/Captn138/mayushii")
        embed.add_field(inline=False, name="ver 0.4.0", value="Fixed intents due to new update of discord.py. Automated with \
            GitHub Actions. Added docstrings. Fixed a few quirks.")
        embed.add_field(inline=False, name="ver 0.3.2", value="Fixed an error in info command, statically added owner_id in \
            MetaInfo class since client.owner_id doesn't work as expected, will be removed when lib is fixed, moved some \
                functions out of BotBasics class.")
        embed.add_field(inline=False, name="ver 0.3.1", value="Changed internal functions, fixed some missing quotes and \
            imports, cleaned unnecessary files.")
        embed.add_field(inline=False, name="ver 0.3.0", value="A lot of rewrites after nearly 2 years of downtime, \
            discord-rewrite.py became discord.py, a lot of commands have been simplified, better handeled some errors, \
                removed useless code, added youy command.")
        embed.add_field(inline=False, name="Ver 0.2.3", value="Added .speedtest command.")
        embed.add_field(inline=False, name="Ver 0.2.2", value="Added .tuturu command.")
        embed.add_field(inline=False, name="Ver 0.2.1", value="Re-implemented autoroles command. 100% working.")
        embed.add_field(inline=False, name="Ver 0.2.0", value="Went from discord.py to discord-rewrite.py. A lot of minimal \
            changes, some upgrades for me to check on the bot, some smoother commands. Added '.clear amount @mention' \
                command. Dropped the autorole command for now. Quite a big update.")
        embed.add_field(inline=False, name="Ver 0.1.3", value="Minor changes.")
        embed.add_field(inline=False, name="Ver 0.1.2", value="Added permissions check to clear and autorole commands.")
        embed.add_field(inline=False, name="Ver 0.1.1", value="Added ping command.")
        embed.add_field(inline=False, name="Ver 0.1.0", value="First Beta release; bot now messages the guild owner on join; \
            added dev command.")
        embed.add_field(inline=False, name="Ver 0.0.2", value="Added clear command.")
        embed.add_field(inline=False, name="Ver 0.0.1", value="First Alpha release, added debug, autorole, okarin, invite, \
            info and help commands; added autoroles on member join, up time and cycling statuses.")
        embed.add_field(inline=False, name="Coming soon", value="Music, reactions roles, autoroles, some guild managment and \
            probably more.")
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete()

    @commands.command(aliases=['i'])
    async def info(self, ctx):
        """Send infos about the bot in chat."""
        logging.info(">>>Called command 'info'")
        embed = discord.Embed(title=f"{self.client.user.name}", description="Cute Mayushii doing her best for ya!",
                              color=0xa1ee33)
        embed.set_author(name=f"{await self.client.fetch_user(MetaInfo.get_owner_id())} 's",
                         icon_url=str((await self.client.fetch_user(MetaInfo.get_owner_id())).avatar_url))
        embed.set_thumbnail(url=MetaInfo.get_embed_thumbnail_url())
        embed.add_field(name="Gild count", value=len(self.client.guilds))
        data = []
        with open(f"./guilds/{ctx.guild.id}.guild", "r") as file:
            data = file.readlines()
        embed.add_field(name="Guild autorole", value=f"{data[0][:-1]} ({data[1]})")
        embed.add_field(inline=False, name="Invite me!", value=MetaInfo.get_bot_invite_link())
        embed.set_footer(text=f"Bot version : {MetaInfo.get_bot_version()}")
        await ctx.send(embed=embed, delete_after=20)
        await ctx.message.delete()

    def help_tuturu(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'tuturu' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}tuturu", value="Plays a nice \"Tuturu\" in your voice \
                    channel. Must be connected to a voice channel.")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}tuturu")
        embed.add_field(inline=False, name="Aliases:", value=f"{command_prefix}t")
        return embed

    def help_youy(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'youy' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}youy", value=f"Displays youy. {__class__.youy_limit} \
                    minutes timeout.")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}youy")
        return embed

    def help_autorole(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'autorole' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}autorole", value="Manage roles lock! Changes the role \
                    given automatically when a new member joins the server.")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}autorole <True/False>")
        embed.add_field(inline=False, name="Aliases:", value=f"{command_prefix}arole")
        embed.add_field(inline=False, name="Warning:", value="You will be asked for a new role name after. You can \
                    cancel the operation.")
        return embed

    def help_kick(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'kick' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}kick", value="Kick members lock! Kicks a member from \
                    the channel.")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}kick <@member> (reason)")
        return embed

    def help_ban(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'ban' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}ban", value="Ban members lock! Bans a member from \
                    the channel")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}ban <@member> (reason)")
        return embed

    def help_unban(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'unban' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}unban", value="Ban members lock! Unbans a member \
                    from the channel")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}unban <Member#xxxx>")
        return embed

    def help_ping(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'ping' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}ping", value="Calculates the bot's ping and sends \
                    it in the channel.")
        return embed

    def help_dev(command_prefix: str, embed: discord.Embed):
        """Generate embed for '' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}dev", value="Shows the development panel, which \
                    contains all the updates history and the upcoming updates.")
        return embed

    def help_clear(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'clear' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}clear", value="Clears a specified amount of messages \
                    in the channel. If used with a @mention, clears an amount of messages from the specified user. Warning : \
                        limit is 500 messages")
        embed.add_field(inline=False, name="Usage:", value=f"{command_prefix}clear (amount) (@mention)")
        embed.add_field(inline=False, name="Aliases:", value=f"{command_prefix}c")
        embed.add_field(inline=False, name="Warning:", value="By default, it will clear the last message")
        return embed

    def help_info(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'info' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}info", value="Gives you infos about the bot: \
                    Creator, uptime, number of guilds and a link to get it.")
        embed.add_field(inline=False, name="Aliases:", value=f"{command_prefix}i")
        return embed

    def help_invite(command_prefix: str, embed: discord.Embed):
        """Generate embed for 'invite' section of help menu.

        Args:
            embed (discord.Embed): The embed in which to add the text.

        Returns:
            discord.Embed: The embed
        """
        embed.add_field(inline=False, name=f"{command_prefix}invite", value="Sends an invite to the Creator's \
                    discord guild.")
        return embed

    @commands.command(aliases=['h'])
    async def help(self, ctx, com: str = None):
        """Send the help menu in chat.

        Args:
            com (str, optional): Command to get help on. Defaults to None.
        """
        command_prefix = await self.client.get_prefix(ctx.message)
        logging.info(f">>>Called command 'help' with argument {com}")
        if com is None:
            embed = discord.Embed(title=f"{self.client.user.name}'s help menu (alias : {command_prefix}h)", description="For \
                details, type .help <argument>. List of commands are:", color=0xa1ee33)
            embed.add_field(inline=False, name="REGULAR COMMANDS", value="=======")
            embed.add_field(inline=False, name=f"{command_prefix}info", value="Gives a little info about the bot.")
            embed.add_field(inline=False, name=f"{command_prefix}help", value="Gives this message.")
            embed.add_field(inline=False, name=f"{command_prefix}invite", value="Gives you an invite link to **Je pars à \
                Gé**.")
            embed.add_field(inline=False, name=f"{command_prefix}dev", value="Shows the development panel.")
            embed.add_field(inline=False, name=f"{command_prefix}ping", value="Gives you the bot's ping.")
            embed.add_field(inline=False, name=f"{command_prefix}tuturu", value="Plays a nice 'Tuturu' in your voice channel")
            embed.add_field(inline=False, name=f"{command_prefix}youy", value="Displays youy")
            embed.add_field(inline=False, name="ADMIN COMMANDS", value="=======")
            embed.add_field(inline=False, name=f"{command_prefix}autorole", value="Change the autorole. Manage roles \
                required.")
            embed.add_field(inline=False, name=f"{command_prefix}clear", value="Clears an amount of messages in the channel. \
                Manage messages required")
            embed.add_field(inline=False, name=f"{command_prefix}kick", value="Kicks a user. Kick members required.")
            embed.add_field(inline=False, name=f"{command_prefix}ban", value="Bans a user. Ban members required.")
            embed.add_field(inline=False, name=f"{command_prefix}unban", value="Unbans a user. Ban members required.")
        else:
            embed = discord.Embed(title=f"{self.client.user.name}'s help menu", description="Specific command:",
                                  color=0xa1ee33)
            match com:
                case "tuturu":
                    embed = Regular.help_tuturu(command_prefix, embed)
                case "youy":
                    embed = Regular.help_youy(command_prefix, embed)
                case "autorole":
                    embed = Regular.help_autorole(command_prefix, embed)
                case "kick":
                    embed = Regular.help_kick(command_prefix, embed)
                case "ban":
                    embed = Regular.help_ban(command_prefix, embed)
                case "unban":
                    embed = Regular.help_unban(command_prefix, embed)
                case "ping":
                    embed = Regular.help_ping(command_prefix, embed)
                case "dev":
                    embed = Regular.help_dev(command_prefix, embed)
                case "clear":
                    embed = Regular.help_clear(command_prefix, embed)
                case "info":
                    embed = Regular.help_info(command_prefix, embed)
                case "invite":
                    embed = Regular.help_invite(command_prefix, embed)
                case _:
                    await ctx.message.delete()
                    return
        await ctx.send(embed=embed)
        await ctx.message.delete()


async def setup(client):
    """Load the class on the bot.

    Args:
        client (discord.ext.commands.bot): The bot on which to load the class.
    """
    await client.add_cog(Regular(client))
