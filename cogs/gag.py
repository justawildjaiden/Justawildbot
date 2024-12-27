from http.client import responses
from re import match

import discord
import json

global response_gag

class GagTypes(discord.ui.View):
    def __init__(self, target):
        super().__init__()
        self.target = target

    @discord.ui.select(
        placeholder= "Please select one",
        min_values=1, #this is the minum amount of options that need to be picked
        max_values=1, #this is the max amount of options allowed
        options=[
            discord.SelectOption(
                label=f'Ball gag',
                description=f'A basic but functional gag'
            ),
            discord.SelectOption(
                label=f'Tape gag',
                description=f'It does the job just right'
            ),
            discord.SelectOption(
                label=f'Sock',
                description=f'A stinky or clean one, just how bad have they been'
            ),
            discord.SelectOption(
                label=f'Dildo gag',
                description=f'2 flies with 1 stone. they train their mouth, and they are silent'
            )
        ]
    )
    async def select_callback(self, select, interation):
        if select.values[0] == f'Ball gag':
            response_gag = f'You picked a ball gag for {self.target.mention}, hope they like balls xd'

        elif select.values[0] == f'Tape gag':
            response_gag = f'You tape {self.target.mention}\'s mouth shut, that\'s gonna hurt to take off'

        elif select.values[0] == f'Sock':
            response_gag = f'You stuff {self.target.mention}\'s mouth with a sock, I hope it\'s clean'

        elif select.values[0] == f'Dildo gag':
            response_gag = f'You shove a dildo in {self.target.mention}\'s mouth, they better get sucking'
        embed = discord.Embed(colour=discord.Colour.green(), title=f'Gag', type='rich',
                              description=f'{response_gag}')
        await interation.response.send_message(embed= embed, ephemeral = True, delete_after= 30)


class Gagging(discord.Cog): #makes a class for the cog that inherts from discord.Cog
    #cogs are used to add functions to the bot, like a module

    def __init__(self,bot): #this method is called when the bot is loaded
        self.bot = bot
    gag= discord.SlashCommandGroup(f'gag',f'A place for all your gag needs',nsfw=True)

    @gag.command(name=f'equip', context= f'guild',
                 description= f'This gives you a list of possible ways to gag a target')
    async def equipgag(self,
                       ctx:discord.ApplicationContext,
                       target:discord.Option(discord.User,name= f'subject', description= f'who do you want to gag', required= True)):
        embed = discord.Embed(colour=discord.Colour.blue(),title=f'Gag',type='rich')
        embed.add_field(name=f'Target',value=f'<@{target.id}>')
        await ctx.respond(embed=embed, view=GagTypes(target=target, timeout=30))
        return

def setup(bot): #this is called by the Pycord to set the cog up
    bot.add_cog(Gagging(bot))