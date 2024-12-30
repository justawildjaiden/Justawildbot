# Importing dependecies
import json
import discord
from enum import Enum

# Defining the file locations
DATABASE_DIRECTORY = "C:/Users/Jaide/Discord-Bot/Database/Guilds"


class GagType(Enum):
    UNEQUIP = "Unequip"
    BALL_GAG = "Ball gag"
    DILDO_GAG = "Dildo gag"
    RING_GAG = "Ring gag"
    REVERSE_DILDO = "Reverse Dildo"
    SOCK = "Sock"
    TAPE = "Tape"
    PACIFIER = "Pacifier"
    UNDERWEAR = "Underwear"


class Gagging_Interface(discord.Cog):
    """Handles gagging-related functionality within Discord bot cog."""

    def __init__(self, bot):
        """Initializes the gagging cog."""
        self.bot = bot

    async def get_gag_levels(ctx: discord.ApplicationContext):
        """Returns a list of gag effects based on the gag type."""
        gag_type_str = ctx.options['type']
        try:
            gag_type = GagType(gag_type_str)
        except ValueError:
            return []

        gag_effects = {
            GagType.UNEQUIP: ["None"],
            GagType.BALL_GAG: ["loose", "tight", "faux"],
            GagType.DILDO_GAG: ["N/A", "faux"],
            GagType.RING_GAG: ["N/A", "faux"],
            GagType.REVERSE_DILDO: ["loose", "tight", "faux"],
            GagType.SOCK: ["loose", "tight", "faux"],
            GagType.TAPE: ["N/A", "faux"],
            GagType.PACIFIER: ["N/A", "faux"],
            GagType.UNDERWEAR: ["loose", "tight", "faux"],
        }
        return gag_effects.get(gag_type, [])

    def _update_user_gag_data(self, user_gag_data, user_need_data, gag_type_str, gag_effect):
        """Updates the user's gag data based on the provided gag type and effect."""
        try:
            gag_type = GagType(gag_type_str)
        except ValueError:
            return

        if gag_type == GagType.UNEQUIP:
            user_gag_data['type'] = None
            user_gag_data['effect'] = None
            user_need_data = False
        else:
            user_gag_data['type'] = gag_type.value
            if gag_effect == "faux":
                user_gag_data['effect'] = None
                user_need_data = False
            else:
                user_gag_data['effect'] = gag_effect
                user_need_data = True
        return user_need_data

    async def changegag(self, ctx: discord.ApplicationContext, gag_type: str, gag_effect: str,
                        target: discord.abc.User):
        """Changes the gag of the targeted user and saves the information to the database."""
        try:
            with open(f'{DATABASE_DIRECTORY}/{ctx.guild.id}.json', "r") as f:
                guild_data = json.load(f)
            user_gag_data = guild_data['members'][str(target.id)]['gag']
            user_need_data = guild_data['members'][str(target.id)]['needtotalk']
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error accessing member data. guild:{ctx.guild.id} id:{target.id} Error: {e}")
            return False

        user_need_data = self._update_user_gag_data(user_gag_data, user_need_data, gag_type, gag_effect)
        guild_data['members'][str(target.id)]['needtotalk'] = user_need_data

        try:
            with open(f'{DATABASE_DIRECTORY}/{ctx.guild.id}.json', "w") as f:
                json.dump(guild_data, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error writing member data. guild:{ctx.guild.id} id:{target.id} Error: {e}")
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

        if target.bot:
            await ctx.respond(content= 'you can\'t gag a bot, you naughty boy', ephemeral=True)
            return None

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
            if target.avatar.url is not None:
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
                                  description=f'Something went wrong, please try again.\n If it keeps happening contact the developer.')
            # Respond with the error embed
            await ctx.respond(embed=embed)
            # Print an error message to the console
            print(f'changegag failed for {target.mention} by {ctx.author.mention}')
            return None


def setup(bot):
    """Loads the gagging cog."""
    bot.add_cog(Gagging_Interface(bot))
