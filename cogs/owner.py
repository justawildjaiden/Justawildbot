import discord
import json

#the location of the guilds folder
folder_location= "C:/Users/Jaide/Discord-Bot/Database/Guilds"

class domming(discord.Cog): #makes a class for the cog that inherts from discord.Cog
    #cogs are used to add functions to the bot, like a module

    def __init__(self,bot): #this method is called when the bot is loaded
        self.bot = bot

    @discord.slash_command(description=f'See the status of the Person', name=f'status', nsfw= True)
    async def status(self,
                     ctx:discord.ApplicationContext,
                     target:discord.Option(discord.User ,required=True, name= f'subject', description=f'mention who you want to see the status of!')):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            with open(f"{folder_location}.json", 'r') as jsonFile:
                data = json.load(jsonFile)
                ids_list = data['ids']
                if ctx.guild.id not in ids_list:
                    embed = discord.Embed(colour=discord.Colour.red(), title=f'ERROR', type='rich',
                                          description=f'Contact dev,\n tell the dev that the guild id isnt procesed in to the storage')
                    await ctx.respond(embed=embed)
            with open(f'{folder_location}/{ctx.guild.id}.json','r') as jsonFile:
                data = json.load(jsonFile)
                data_user = data['members'][f'{target.id}']
                await ctx.respond(f'{data_user}')




def setup(bot): #this is called by the Pycord to set the cog up
    bot.add_cog(domming(bot))