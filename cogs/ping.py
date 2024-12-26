import discord
from discord import DMChannel


class Latency(discord.Cog): #makes a class for the cog that inherts from discord.Cog
    #cogs are used to add functions to the bot, like a module

    def __init__(self,bot): #this method is called when the bot is loaded
        self.bot = bot
    # this command responds with the latency of the bot

    @discord.slash_command(description=f'Sends the latency of the bot', name=f'ping')
    async def latency_cmd(self, ctx):
        ping = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blue(), title=f'Pong!', type='rich',
                              description=f'The latency is {ping}ms')
        await ctx.respond(embed=embed)
        print(f'{ping}ms')

def setup(bot): #this is called by the Pycord to set the cog up
    bot.add_cog(Latency(bot))