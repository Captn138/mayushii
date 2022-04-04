import discord, logging
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['c'])
    async def clear(self, ctx, amount: int = 1, userArg = None):
        if ctx.message.author.guild_permissions.manage_messages == True:
            logging.info(f">>>Called command 'clear' with argument {amount} : {ctx.message.author}")
            if userArg != None:
                logging.info(f" Targeted user: {userArg}")
                userid = str(userArg)[3:-1]
                await ctx.message.delete()
                async for message in ctx.channel.history(limit = 500):
                    counter = 0
                    if int(message.author.id) == int(userid):
                        counter += 1
                        if counter <= amount+1:
                            await message.delete()
            else:
                await ctx.channel.purge(limit = amount+1)
            await ctx.send(f"I have deleted {amount} messages for ya!", delete_after = 5)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        if ctx.message.author.guild_permissions.kick_members == True:
            logging.info(f">>>Called command 'kick' of {member} with reason '{reason}' : {ctx.message.author}")
            await member.kick(reason = reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        if ctx.message.author.guild_permissions.ban_members == True:
            logging.info(f">>>Called command 'ban' of {member} with reason '{reason}' : {ctx.message.author}")
            await member.ban(reason = reason)

    @commands.command()
    async def unban(self, ctx, *, member):
        if ctx.message.author.guild_permissions.ban_members == True:
            logging.info(f">>>Called command 'unban' of {member} : {ctx.message.author}")
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discirminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    return

    @commands.command(aliases = ['arole'])
    async def autorole(self, ctx, var = 'True'):
        if ctx.message.author.guild_permissions.manage_roles == True:
            logging.info(f">>>Called command 'autorole' on [{ctx.guild}] with argument {var} : {ctx.message.author}")
            data = []
            with open(f"./guilds/{ctx.guild.id}.guild", "r") as file:
                data = file.readlines()
            if var == 'False':
                with open(f"./guilds/{ctx.guild.id}.guild", "w") as file:
                    file.write(data[0])
                    file.write("False")
                await ctx.send("Autoroles have been disabled", delete_after = 5)
            elif var == 'True':
                await ctx.send("Type the new autorole, or type 'cancel' to cancel the operation", delete_after = 15)
                answer = await self.client.wait_for('message', timeout = 15)
                if answer.content == 'cancel':
                    await ctx.send("Canceled!", delete_after = 5)
                    await answer.delete()
                    return
                else:
                    with open(f"./guilds/{ctx.guild.id}.guild", "w") as file:
                        file.write(f"{answer.content}\nTrue")
                    await ctx.send(f"Autoroles have been changed to {answer.content}", delete_after = 5)

def setup(client):
    client.add_cog(Admin(client))
