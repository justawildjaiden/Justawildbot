import discord
import json

#Defining the file locations
file_location = "C:/Users/Jaide/Discord-Bot/Database/Guilds"

class Gagging(discord.Cog):
    """Cog for gagging commands (NSFW)."""

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

        # Handles file not found and JSON decode errors
        except FileNotFoundError:
            print(f"Error: Member data file not found. guild:{ctx.guild.id} id:{target.id} ")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in member data file. guild:{ctx.guild.id} id:{target.id}")
            return False

        # Modifies the user's gag data based on the provided gag type and efect
        if gag_type == "Unequip":
            user_gag_data['gag_type'] = "Unequip"
            user_gag_data['gag_effect'] = None  # Sets the effect to None when unequipping
        else:
            user_gag_data['gag_type'] = gag_type
            # If the gag effect is "faux", set the effect to None.
            if gag_effect == "faux":
                user_gag_data['gag_effect'] = None
            else:
                user_gag_data['gag_effect'] = gag_effect

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
                                             description=f'not required')
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

        if changegag(ctx, gag_type, gag_effect, target):
            if gag_type is not "Unequip":
                ctx.respond(f'gaged {target.mention}')
                return None

            elif gag_type is "Unequip":
                ctx.respond(f'ungaged {target.mention}')
                return None

        else:
            ctx.respond(f'gag failed, try again else contact the developer')
            print(f'changegag failed for {target.mention} by {ctx.author.mention}')
            return None


def setup(bot):
    """Loads the gagging cog."""
    bot.add_cog(Gagging(bot))
