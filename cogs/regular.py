import discord
from discord.ext import commands
import asyncio

meta = open("meta.txt", "r").readlines()

class Regular(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def tuturu(self, ctx):
        destination = ctx.message.author.voice.channel
        vc = await destination.connect()
        vc.play(discord.FFmpegPCMAudio('tuturu.mp3'))
        await asyncio.sleep(2)
        await vc.disconnect()

    @commands.command()
    async def invite(self, ctx):
        print(">>>Called command 'invite'")
        await ctx.message.delete()
        bot_message = await ctx.send(f"Here's an invite link to my creator's server! Link will be removed in 15 seconds: {meta[2]}")
        await bot_message.delete(delay = 15)

    @commands.command()
    async def ping(self, ctx):
        print(">>>Called command 'ping'")
        await ctx.send(f'Pong! [{round(self.client.latency*1000)}ms]', delete_after = 3)
        await ctx.message.delete(delay = 3)

    @commands.command()
    async def dev(self, ctx):
        print(">>>Called command 'dev'")
        embed = discord.Embed(title = "Mayushii ☆'s dev history", description = "All my updates should be here.", color = 0xa1ee33)
        embed.set_thumbnail(url = meta[3])
        embed.add_field(name = "Ver 0.2.1", value = "Re-implemented autoroles command. 100% working", inline = False)
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
        print(">>>Called command 'info'")
        embed = discord.Embed(title = "Mayushii ☆", description = "Cute Mayushii doing her best for ya!", color = 0xa1ee33)
        embed.set_author(name = "Captn138#0505 's", icon_url = meta[4])
        embed.set_thumbnail(url = meta[3])
        embed.add_field(name = "Gild count", value = len(self.client.guilds))
        data = []
        with open(f"./guilds/{ctx.guild.id}.txt", "r") as file:
            data = file.readlines()
        embed.add_field(name = "Guild autorole", value = f"{data[0][:-1]} ({data[1]})")
        embed.add_field(name = "Invite", value = meta[1], inline = False)
        embed.set_footer(text = "Bot version : {}".format(meta[0]))
        await ctx.send(embed = embed, delete_after = 20)
        await ctx.message.delete()

    @commands.command(aliases = ['h'])
    async def help(self, ctx, com = "NULL"):
        print(f">>>Called command 'help' with argument {com}")
        if com == "NULL":
            embed = discord.Embed(title = "Mayushii ☆'s help menu (alias : .h)", description = "For details, type .help <argument>. List of commands are:", color = 0xa1ee33)
            embed.add_field(name = ".info", value = "Gives a little info about the bot.", inline = False)
            embed.add_field(name = ".help", value = "Gives this message.", inline = False)
            embed.add_field(name = ".invite", value = "Gives you an invite link to **Je pars à Gé**.", inline = False)
            embed.add_field(name = ".dev", value = "Shows the development panel.", inline = False)
            embed.add_field(name = ".ping", value = "Gives you the bot's ping.", inline = False)
            embed.add_field(name = ".autorole", value = "Change the autorole. Manage roles required.", inline = False)
            embed.add_field(name = ".clear", value = "Clears an amount of messages in the channel. Manage messages required", inline = False)
            embed.add_field(name = ".kick", value = "Kicks a user. Kick members required.", inline = False)
            embed.add_field(name = ".ban", value = "Bans a user. Ban members required.", inline = False)
            embed.add_field(name = ".unban", value = "Unbans a user. Ban members required.", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "autorole":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".autorole", value = "Manage roles lock! Changes the role given automatically when a new member joins the server.", inline = False)
            embed.add_field(name = "Usage:", value = ".autorole <True/False>", inline = False)
            embed.add_field(name = "Aliases:", value = ".arole", inline = False)
            embed.add_field(name = "Warning:", value = "You will be asked for a new role name after. You can cancel the operation.", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "kick":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".kick", value = "Kick members lock! Kicks a member from the channel", inline = False)
            embed.add_field(name = "Usage:", value = ".kick <@member> (reason)", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "ban":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".ban", value = "Ban members lock! Bans a member from the channel", inline = False)
            embed.add_field(name = "Usage:", value = ".ban <@member> (reason)", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "unban":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".unban", value = "Ban members lock! Unbans a member from the channel", inline = False)
            embed.add_field(name = "Usage:", value = ".unban <Member#xxxx>", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "ping":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".ping", value = "Calculates the bot's ping and sends it in the channel.", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "dev":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".dev", value = "Shows the development panel, which contains all the updates history and the upcoming updates.", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "clear":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".clear", value = "Clears a specified amount of messages in the channel. If used with a @mention, clears an amount of messages from the specified user. Warning : limit is 500 messages", inline = False)
            embed.add_field(name = "Usage:", value = ".clear (amount) (@mention)", inline = False)
            embed.add_field(name = "Aliases:", value = ".c", inline = False)
            embed.add_field(name = "Warning:", value = "By default, it will clear the last message", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "info":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".info", value = "Gives you infos about the bot: Creator, uptime, number of guilds and a link to get it.")
            embed.add_field(name = "Aliases:", value = ".i", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "invite":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".invite", value = "Sends an invite to the Creator's discord guild.")
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "clear":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".clear", value = "Clears a number of messages in the channel. Default is 1.", inline = False)
            embed.add_field(name = "Usage:", value = ".clear [number]", inline = False)
            await ctx.send(embed = embed, delete_after = 10)
        elif com == "autorole":
            embed = discord.Embed(title = "Mayushii ☆'s help menu", description = "Specific command:", color = 0xa1ee33)
            embed.add_field(name = ".autorole", value = "ADMIN LOCK! Changes the role given automatically when a new member joins the guild.")
            embed.add_field(name = "Usage:", value = ".autorole <true/false>")
            embed.add_field(name = "Warning:", value = "You will be asked for a new role name after. You can cancel the operation.")
            await ctx.send(embed = embed, delete_after = 10)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Regular(client))