import discord
import json

# Location of the guilds folder
folder_location = "C:/Users/Jaide/Discord-Bot/Database/Guilds"


class status(discord.Cog):
    """Cog for displaying the status of a user."""

    def __init__(self, bot):
        """Initializes the cog with the bot instance."""
        self.bot = bot

    @discord.slash_command(description="See the status of the Person", name="status", nsfw=True, context='guild')
    async def status(self,
                     ctx: discord.ApplicationContext,
                     target: discord.Option(discord.User, required=True, name='subject',
                                            description='Mention who you want to see the status of!')):
        """
        Slash command to display the status of a mentioned user.

        Args:
            ctx: The application context.
            target: The Discord user whose status is to be displayed.
        """

        guilds_filepath = f"{folder_location}.json"  # corrected file path

        try:
            with open(guilds_filepath, 'r') as f:
                guild_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Guilds file not found: {guilds_filepath}")  # More helpful debug message
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description="Guild data file not found. Please contact the developer.")
            await ctx.respond(embed=embed)
            return  # Stop processing if the file isn't found

        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in guilds file: {guilds_filepath}")
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description="Invalid guild data. Please contact the developer.")
            await ctx.respond(embed=embed)
            return

        ids_list = guild_data.get('ids', [])  # Use .get() to handle missing 'ids' key
        if ctx.guild.id not in ids_list:
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description="This guild is not registered. Please contact the developer.")
            await ctx.respond(embed=embed)
            return

        members_filepath = f'{folder_location}/{ctx.guild.id}.json'
        try:
            with open(members_filepath, 'r') as f:
                member_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Member data file not found. guild:{ctx.guild.id} id:{target.id} ")
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description="Member data file not found. Please contact the developer.")
            await ctx.respond(embed=embed)
            return
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in member data file. guild:{ctx.guild.id} id:{target.id}")
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description="Invalid member data. Please contact the developer.")
            await ctx.respond(embed=embed)
            return

        try:
            target_id_str = str(target.id)  # convert to string for dictionary key
            data_user = member_data['members'][target_id_str]
            await ctx.respond(f'{data_user}')

        except KeyError as e:
            print(f"Error: Key not found in member data: {e}")
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description=f"User data not found. {e}")  # More informative error message
            await ctx.respond(embed=embed)


def setup(bot):
    """Loads the cog."""
    bot.add_cog(status(bot))