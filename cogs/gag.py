#Importing dependecies
import json

import discord

#Defining the file locations
file_location = "C:/Users/Jaide/Discord-Bot/Database/Guilds"

class Gagging(discord.Cog):
    """
    Handles gagging-related functionality within Discord bot cog.

    This cog is responsible for providing functionality related to gagging,
    such as retrieving available gag levels and changing the gag settings
    for a specific user. It manages the gag types and their respective options,
    as well as interacting with and modifying relevant data stored in JSON files.

    This cog does not provide any text editing functionality, that needs to be done in a seprate cog.

    :ivar bot: The Discord bot instance that this cog belongs to.
    :type bot: discord.Bot
    """

    def __init__(self, bot):
        """Initializes the gagging cog."""
        self.bot = bot

    async def get_gag_levels(ctx: discord.ApplicationContext):
        """
        Depending on what type of gag you put on the user, you get different options of effects
        """
        # Get the gag type from user input
        gag_type = ctx.options['type']

        # Return a list of gag effects based on the gag type
        if gag_type == "Unequip":
            return ["None"]
        elif gag_type == "Ball gag":
            return ["loose", "tight", "extreme", "faux"]
        elif gag_type == "Dildo gag":
            return ["N/A", "faux"]
        elif gag_type == "Ring gag":
            return ["not_applicable", "faux"]
        elif gag_type == "Reverse Dildo":
            return ["loose", "tight", "faux"]
        elif gag_type == "Sock":
            return ["loose", "tight", "faux"]
        elif gag_type == "Tape":
            return ["not_applicable", "faux"]
        elif gag_type == "Pacifier":
            return ["not_applicable", "faux"]
        elif gag_type == "Underwear":
            return ["loose", "tight", "faux"]
        else:
            return []

    async def changegag(self,
                        ctx: discord.ApplicationContext,
                        gag_type:str,
                        gag_effect:str,
                        target:discord.abc.User):
        """
            This function changes the gag of the user that is being targeted.
            It saves this information to the database.

            Args:
                ctx: The application context.
                gag_type: The type of gag to apply.
                gag_effect: The effect of the gag.
                target: The user to gag.

            Returns:
                bool: True if the gag was successfully changed, False otherwise.
        """

        # Attempts to open and read the guild's JSON file
        try:
            with open(f'{file_location}/{ctx.guild.id}.json', "r") as f:
                guild_data = json.load(f)

            # Accesses the user's gag data within the guild data
            user_gag_data = guild_data['members'][str(target.id)]['gag']
            user_need_data = guild_data['members'][str(target.id)]['needtotalk']

        # Handles file not found and JSON decode errors
        except FileNotFoundError:
            print(f"Error: Member data file not found. guild:{ctx.guild.id} id:{target.id} ")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in member data file. guild:{ctx.guild.id} id:{target.id}")
            return False

        # Modifies the user's gag data based on the provided gag type and efect
        if gag_type == "Unequip":
            user_gag_data['type'] = None    # Sets the type to None
            user_gag_data['effect'] = None  # Sets the effect to None
            user_need_data = False          # Sets the need to talk for to False
        else:
            user_gag_data['type'] = gag_type
            # If the gag effect is "faux", set the effect to None.
            # and changes the need to be talked for to false
            if gag_effect == "faux":
                user_gag_data['effect'] = None
                user_need_data = False

            #sets the gag_effect and set need to talk to true
            else:
                user_gag_data['effect'] = gag_effect
                user_need_data = True

        # Attempts to write the updated guild data back to the JSON file
        try:
            with open(f'{file_location}/{ctx.guild.id}.json', "w") as f:
                json.dump(guild_data, f, indent=4)

        # Handles file not found and JSON decode errors during write operation
        except FileNotFoundError:
            print(f"Error: Member data file not found. guild:{ctx.guild.id} id:{target.id} ")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in member data file. guild:{ctx.guild.id} id:{target.id}")
            return False

        return True



    @discord.slash_command(description="gags the mentioned user", name="gag", context='guild', nsfw=True)
    async def gag(self,
                  ctx: discord.ApplicationContext,
                  target: discord.Option(discord.User,
                                         required=True,
                                         name="target",
                                         description="who do you want to gag"),
                  gag_type: discord.Option(str,
                                           choices=[
                                                        "Unequip",
                                                        "Ball gag",
                                                        "Dildo gag",
                                                        "Ring gag",
                                                        "Reverse Dildo",
                                                        "Sock",
                                                        "Tape",
                                                        "Pacifier",
                                                        "Underwear"
                                                    ],
                                            required=True,
                                            name="type",
                                            description="What kind of gag do you want to put on the user?"),
                  gag_effect: discord.Option(str,
                                             required=True,
                                             name="effect",
                                             description="What effect do you want to the gag to have",
                                             autocomplete=discord.utils.basic_autocomplete(get_gag_levels)
                                             ),
                  gag_reason: discord.Option(str,
                                             required=False,
                                             name=f'reason',
                                             description=f'not required',
                                             default=None)
                  ):
        """
                Applies a gag to the specified user.

                Args:
                    ctx: The application context.
                    target: The user to gag.
                    gag_type: The type of gag to apply.
                    gag_effect: The effect of the gag.
                    gag_reason: The reason for gagging the user (optional).
                """

        # If the gag was successfully changed
        if await self.changegag(ctx, gag_type, gag_effect, target):
            # If the gag type is not "Unequip" (meaning a gag is being applied)
            if gag_type != "Unequip":
                # Create an embed message to display the gag application
                embed = discord.Embed(
                    color=discord.Color.blurple(),
                    title=f'**Gag**',
                    description=f'{ctx.author.mention} puts a gag on {target.mention}'
                )
                # Add fields for gag type and effect
                embed.add_field(name="what type?", value=str(gag_type), inline=True)
                embed.add_field(name="How tight?", value=str(gag_effect), inline=True)

            # If the gag type is "Unequip" (meaning a gag is being removed)
            elif gag_type == "Unequip":
                # Create an embed message to display the gag removal
                embed = discord.Embed(
                    color=discord.Color.blurple(),
                    title=f'**Ungag**',
                    description=f'{ctx.author.mention} takes the gag of {target.mention}'
                )
            # Add an optional field for the gag reason if provided
            if gag_reason is not None:
                embed.add_field(name="Why?", value=str(gag_reason), inline=False)
            # Set the thumbnail of the embed using the target's avatar, if available
            if ctx.author.avatar is not None:
                try:
                    embed.set_thumbnail(url=target.avatar.url)
                except:
                    nothing = None  # Placeholder for error handling, no action taken

            # Set the footer of the embed using the author's avatar and name, if available
            if ctx.author.avatar is not None:
                try:
                    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                except:
                    embed.set_footer(text=f"Requested by {ctx.author.name}")  # Fallback in case the avatar URL fails
            
            # Respond with the embed message
            await ctx.respond(embed=embed)
            return None

        # If the gag change failed
        else:
            # Create an error embed message
            embed = discord.Embed(colour=discord.Colour.red(), title="ERROR",
                                  description=f'Something went wrong, please try again.\n{None
                                  }             If it keeps happening contact the developer.')
            # Respond with the error embed
            await ctx.respond(embed=embed)
            # Print an error message to the console
            print(f'changegag failed for {target.mention} by {ctx.author.mention}')
            return None


def setup(bot):
    """Loads the gagging cog."""
    bot.add_cog(Gagging(bot))
