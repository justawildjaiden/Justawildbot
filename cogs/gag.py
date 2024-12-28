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
