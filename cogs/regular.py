import discord, asyncio, datetime, logging
from discord.ext import commands
from bot import BotBasics
from meta import MetaInfo as MI


class Regular(commands.Cog):

    last_youy: datetime.datetime = None
    youy_limit = 5

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['t']) #DEPRECATED
    async def tuturu(self, ctx):
        logging.info(">>>Called command 'tuturu'")
        destination = ctx.message.author.voice.channel
        vc = await destination.connect()
        vc.play(discord.FFmpegPCMAudio('tuturu.mp3'))
        await asyncio.sleep(2)
        await vc.disconnect()

    @commands.command()
    async def youy(self, ctx):
        logging.info(">>>Called command 'youy'")
        days, hours, minutes, seconds = BotBasics.deltatime(__class__.last_youy)
        if __class__.last_youy is None or (days*24*60)+(hours*60)+minutes > __class__.youy_limit:
           __class__.last_youy = datetime.datetime.utcnow()
           await ctx.send("https://media.discordapp.net/attachments/622011856642637825/622012196397776896/JPEG_20181001_113150.jpg")

    @commands.command()
    async def invite(self, ctx):
        logging.info(">>>Called command 'invite'")
        await ctx.message.delete()
        bot_message = await ctx.send(f"Here's an invite link to my creator's server! Link will be removed in 15 seconds: {MI.get_owner_server_invite_link()}")
        await bot_message.delete(delay = 15)

    @commands.command()
    async def ping(self, ctx):
        logging.info(">>>Called command 'ping'")
        await ctx.send(f'Pong! [{round(self.client.latency*1000)}ms]', delete_after = 3)
        await ctx.message.delete(delay = 3)

    @commands.command()
    async def dev(self, ctx):
        logging.info(">>>Called command 'dev'")
        embed = discord.Embed(title = f"{self.client.user.name}'s dev history", description = "All my updates should be here.", color = 0xa1ee33)
        embed.set_thumbnail(url = MI.get_embed_thumbnail_url())
        embed.add_field(name = "Source code", value = "https://github.com/Captn138/mayushii")
        embed.add_field(name = "ver 0.3.2", value = "Fixed a snowflake error in info command, statically added owner_id in MetaInfo class since client.owner_id doesn't work as expected, will be removed when lib is fixed, moved some functions out of BotBasics class")
        embed.add_field(name = "ver 0.3.1", value = "Changed internal functions, fixed some missing quotes and imports, cleaned unnecessary files")
        embed.add_field(name = "ver 0.3.0", value = "A lot of rewrites after nearly 2 years of downtime, discord-rewrite.py became discord.py, a lot of commands have been simplified, better handeled some errors, removed useless code, added youy command")
        embed.add_field(name = "Ver 0.2.3", value = "Added .speedtest command.", inline = False)
        embed.add_field(name = "Ver 0.2.2", value = "Added .tuturu command.", inline = False)
        embed.add_field(name = "Ver 0.2.1", value = "Re-implemented autoroles command. 100% working.", inline = False)
        embed.add_field(name = "Ver 0.2.0", value = "Went from discord.py to discord-rewrite.py. A lot of minimal changes, some upgrades for me to check on the bot, some smoother commands. Added '.clear amount @mention' command. Dropped the autorole command for now. Quite a big update.", inline = False)
        embed.add_field(name = "Ver 0.1.3", value = "Minor changes.", inline = False)
        embed.add_field(name = "Ver 0.1.2", value = "Added permissions check to clear and autorole commands.", inline = False)
        embed.add_field(name = "Ver 0.1.1", value = "Added ping command.", inline = False)
        embed.add_field(name = "Ver 0.1.0", value = "First Beta release; bot now messages the guild owner on join; added dev command.", inline = False)
        embed.add_field(name = "Ver 0.0.2", value = "Added clear command.", inline = False)
        embed.add_field(name = "Ver 0.0.1", value = "First Alpha release, added debug, autorole, okarin, invite, info and help commands; added autoroles on member join, up time and cycling statuses.", inline = False)
        embed.add_field(name = "Coming soon", value = "Music, reactions roles, autoroles, some guild managment and probably more.", inline = False)
        await ctx.send(embed = embed, delete_after = 20)
        await ctx.message.delete()

    @commands.command(aliases = ['i'])
    async def info(self, ctx):
        logging.info(">>>Called command 'info'")
        embed = discord.Embed(title = f"{self.client.user.name}", description = "Cute Mayushii doing her best for ya!", color = 0xa1ee33)
        embed.set_author(name = f"{await self.client.fetch_user(MI.get_owner_id())} 's", icon_url = str((await self.client.fetch_user(MI.get_owner_id())).avatar_url))
        embed.set_thumbnail(url = MI.get_embed_thumbnail_url())
        embed.add_field(name = "Gild count", value = len(self.client.guilds))
        data = []
        with open(f"./guilds/{ctx.guild.id}.guild", "r") as file:
            data = file.readlines()
        embed.add_field(name = "Guild autorole", value = f"{data[0][:-1]} ({data[1]})")
        embed.add_field(name = "Invite", value = MI.get_owner_server_invite_link(), inline = False)
        embed.set_footer(text = f"Bot version : {MI.get_bot_version()}")
        await ctx.send(embed = embed, delete_after = 20)
        await ctx.message.delete()

    @commands.command(aliases = ['h'])
    async def help(self, ctx, com = None):
        command_prefix = await self.client.get_prefix(ctx.message)
        logging.info(f">>>Called command 'help' with argument {com}")
        if com is None:
            embed = discord.Embed(title = f"{self.client.user.name}'s help menu (alias : {command_prefix}h)", description = "For details, type .help <argument>. List of commands are:", color = 0xa1ee33)
            embed.add_field(name = "REGULAR COMMANDS", value = "=======", inline = False)
            embed.add_field(name = f"{command_prefix}info", value = "Gives a little info about the bot.", inline = False)
            embed.add_field(name = f"{command_prefix}help", value = "Gives this message.", inline = False)
            embed.add_field(name = f"{command_prefix}invite", value = "Gives you an invite link to **Je pars à Gé**.", inline = False)
            embed.add_field(name = f"{command_prefix}dev", value = "Shows the development panel.", inline = False)
            embed.add_field(name = f"{command_prefix}ping", value = "Gives you the bot's ping.", inline = False)
            embed.add_field(name = f"{command_prefix}tuturu", value = "Plays a nice \"Tuturu\" in your voice channel", inline = False)
            embed.add_field(name = "ADMIN COMMANDS", value = "=======", inline = False)
            embed.add_field(name = f"{command_prefix}autorole", value = "Change the autorole. Manage roles required.", inline = False)
            embed.add_field(name = f"{command_prefix}clear", value = "Clears an amount of messages in the channel. Manage messages required", inline = False)
            embed.add_field(name = f"{command_prefix}kick", value = "Kicks a user. Kick members required.", inline = False)
            embed.add_field(name = f"{command_prefix}ban", value = "Bans a user. Ban members required.", inline = False)
            embed.add_field(name = f"{command_prefix}unban", value = "Unbans a user. Ban members required.", inline = False)
        else:
            embed = discord.Embed(title = f"{self.client.user.name}'s help menu", description = "Specific command:", color = 0xa1ee33)
            if com == "tuturu":
                embed.add_field(name = f"{command_prefix}tuturu", value = "Plays a nice \"Tuturu\" in your voice channel. Must be connected to a voice channel.", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}tuturu", inline = False)
                embed.add_field(name = "Aliases:", value = f"{command_prefix}t", inline = False)
            elif com == "autorole":
                embed.add_field(name = f"{command_prefix}autorole", value = "Manage roles lock! Changes the role given automatically when a new member joins the server.", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}autorole <True/False>", inline = False)
                embed.add_field(name = "Aliases:", value = f"{command_prefix}arole", inline = False)
                embed.add_field(name = "Warning:", value = "You will be asked for a new role name after. You can cancel the operation.", inline = False)
            elif com == "kick":
                embed.add_field(name = f"{command_prefix}kick", value = "Kick members lock! Kicks a member from the channel.", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}kick <@member> (reason)", inline = False)
            elif com == "ban":
                embed.add_field(name = f"{command_prefix}ban", value = "Ban members lock! Bans a member from the channel", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}ban <@member> (reason)", inline = False)
            elif com == "unban":
                embed.add_field(name = f"{command_prefix}unban", value = "Ban members lock! Unbans a member from the channel", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}unban <Member#xxxx>", inline = False)
            elif com == "ping":
                embed.add_field(name = f"{command_prefix}ping", value = "Calculates the bot's ping and sends it in the channel.", inline = False)
            elif com == "dev":
                embed.add_field(name = f"{command_prefix}dev", value = "Shows the development panel, which contains all the updates history and the upcoming updates.", inline = False)
            elif com == "clear":
                embed.add_field(name = f"{command_prefix}clear", value = "Clears a specified amount of messages in the channel. If used with a @mention, clears an amount of messages from the specified user. Warning : limit is 500 messages", inline = False)
                embed.add_field(name = "Usage:", value = f"{command_prefix}clear (amount) (@mention)", inline = False)
                embed.add_field(name = "Aliases:", value = f"{command_prefix}c", inline = False)
                embed.add_field(name = "Warning:", value = "By default, it will clear the last message", inline = False)
            elif com == "info":
                embed.add_field(name = f"{command_prefix}info", value = "Gives you infos about the bot: Creator, uptime, number of guilds and a link to get it.")
                embed.add_field(name = "Aliases:", value = f"{command_prefix}i", inline = False)
            elif com == "invite":
                embed = discord.Embed(title = f"{self.client.user.name}'s help menu", description = "Specific command:", color = 0xa1ee33)
                embed.add_field(name = f"{command_prefix}invite", value = "Sends an invite to the Creator's discord guild.")
            else:
                await ctx.message.delete()
                return
        await ctx.send(embed = embed)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Regular(client))
