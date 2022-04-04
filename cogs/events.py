import discord, os
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == False:
            print(f'>>>>>[{member.guild}] New member: {member}')
            data = []
            for filename in os.listdir('./guilds'):
                if filename == f'{member.guild.id}.guild':
                    with open(f'./guilds/{filename}', 'r') as file:
                        data = file.readlines()
            if data[1] == 'True':
                role = discord.utils.get(member.guild.roles, name = data[0][:-1])
                await member.add_roles(role)
        else:
            print(f'>>>>>[{member.guild}] New bot: {member}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(f"./guilds/{guild.id}.guild", "w+") as file:
            file.write("\nFalse")
        await guild.owner.send(f"Tuturuuu! I'm {self.client.user.name}! Thanks for adding me to your guild! My prefix is **{self.client.get_prefix()}**. Don't forget to place my role on top of all the others so I can work properly.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        passerrors = (commands.CommandNotFound, commands.MissingRequiredArgument)
        if isinstance(error, passerrors):
            pass
        elif isinstance(error, commands.CommandInvokeError):
            print(f"Exception on command '{ctx.message.content}':\n\t{error}")

def setup(client):
    client.add_cog(Events(client))
