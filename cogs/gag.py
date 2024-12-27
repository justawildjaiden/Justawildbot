import discord
import json

class GagTypes(discord.ui.View):
    def __init__(self, target=None,timeout=None,author=None,response_gag=None,guild=None):
        super().__init__()
        self.target = target
        self.timeout= timeout
        self.author = author
        self.response_gag = response_gag
        self.guild = guild

    async def on_timeout(self):
        self.disable_all_items()

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
            self.response_gag = f'{self.author.mention} picked a ball gag for {self.target.mention}, hope they like balls xd'

        elif select.values[0] == f'Tape gag':
            self.response_gag = f'{self.author.mention} tapes {self.target.mention}\'s mouth shut, that\'s gonna hurt to take off'

        elif select.values[0] == f'Sock':
            self.response_gag = f'{self.author.mention} stuffs {self.target.mention}\'s mouth with a sock, I hope it\'s clean'

        elif select.values[0] == f'Dildo gag':
            self.response_gag = f'{self.author.mention} shoves a dildo in {self.target.mention}\'s mouth, they better get sucking'

        if self.change_gag(select):
            embed = discord.Embed(colour=discord.Colour.green(), title=f'Gag', type='rich',
                                  description=f'{self.response_gag}')
            await interation.response.send_message(embed= embed, ephemeral = False)
        else:
            embed = discord.Embed(colour=discord.Colour.red(), title=f'ERROR', type='rich',
                                  description=f'Changing gag error, try aigan if that fails, contact dev')
            await interation.response.send_message(embed=embed, ephemeral=True)

    def change_gag(self, select):  # Updated change_gag function
        try:
            filepath = f'C:/Users/Jaide/Discord-Bot/Database/Guilds/{self.guild}.json'
            with open(filepath, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file: {filepath}")
            return False

        try:
            target_id_str = str(self.target.id)
            if 'members' not in data:
                print(f"Error: 'members' key not found in JSON data.")
                return False
            if target_id_str not in data['members']:
                data['members'][target_id_str] = {}

            data['members'][target_id_str]['gag'] = select.values[0]

        except KeyError as e:
            print(f"Error: Key not found in JSON: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False

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
        await ctx.respond(embed=embed, view=GagTypes(target=target, timeout=30,author=ctx.author,guild=ctx.guild.id), ephemeral = True, delete_after= 30)
        return

def setup(bot): #this is called by the Pycord to set the cog up
    bot.add_cog(Gagging(bot))