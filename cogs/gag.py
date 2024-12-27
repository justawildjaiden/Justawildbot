import discord
import json


class GagTypes(discord.ui.View):
    """View for selecting a gag type."""

    def __init__(self, target: discord.User, timeout: int, author: discord.User, response_gag: str, guild: int,
                 interaction: discord.Interaction):
        """Initializes the GagTypes view.

        Args:
            target: The user to be gagged.
            timeout: Timeout for the view.
            author: User initiating the gag.
            response_gag: Initial response message.
            guild: ID of the guild.
            interaction: The interaction object.
        """
        super().__init__(timeout=timeout)
        self.target = target
        self.timeout = timeout
        self.author = author
        self.response_gag = response_gag
        self.guild = guild
        self.interaction = interaction

    async def on_timeout(self):
        """Edits the original ephemeral message with a timeout notification."""
        self.disable_all_items()

        timeout_embed = discord.Embed(colour=discord.Colour.red(), title="Timed out!",
                                      description="You didn't select a gag in time.")
        try:
            await self.interaction.edit_original_response(embed=timeout_embed, view=None)
        except discord.NotFound:
            channel_id = self.interaction.channel_id
            guild_id = self.interaction.guild_id
            print(
                f"Original interaction not found in guild {guild_id}, channel {channel_id}. It may have been deleted.")
        except discord.HTTPException as e:
            print(f"Error editing interaction: {e}")

    @discord.ui.select(
        placeholder="Please select one",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label='Ball gag', description='A basic but functional gag'),
            discord.SelectOption(label='Tape gag', description='It does the job just right'),
            discord.SelectOption(label='Sock', description='A stinky or clean one, just how bad have they been'),
            discord.SelectOption(label='Dildo gag',
                                 description='2 flies with 1 stone. they train their mouth, and they are silent')
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        """Callback for when a gag type is selected.

        Args:
            select: The select option chosen.
            interaction: The interaction object.
        """
        if select.values[0] == 'Ball gag':
            self.response_gag = f'{self.author.mention} picked a ball gag for {self.target.mention}, hope they like balls xd'
        elif select.values[0] == 'Tape gag':
            self.response_gag = f'{self.author.mention} tapes {self.target.mention}\'s mouth shut, that\'s gonna hurt to take off'
        elif select.values[0] == 'Sock':
            self.response_gag = f'{self.author.mention} stuffs {self.target.mention}\'s mouth with a sock, I hope it\'s clean'
        elif select.values[0] == 'Dildo gag':
            self.response_gag = f'{self.author.mention} shoves a dildo in {self.target.mention}\'s mouth, they better get sucking'

        if self.change_gag(select):
            embed = discord.Embed(colour=discord.Colour.green(), title='Gag', description=self.response_gag)
            await interaction.response.send_message(embed=embed, ephemeral=False)  # this should be ephemeral as well
        else:
            embed = discord.Embed(colour=discord.Colour.red(), title='ERROR',
                                  description='Changing gag error, try again if that fails, contact dev')
            await interaction.response.send_message(embed=embed, ephemeral=True)

    def change_gag(self, select):
        """Changes the gag for the target user in the JSON file.

        Args:
            select: The select option containing the new gag.
        """

        filepath = f'C:/Users/Jaide/Discord-Bot/Database/Guilds/{self.guild}.json'
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:  # Combined exception handling
            print(f"Error reading from file: {e}")
            return False

        try:
            target_id_str = str(self.target.id)
            if 'members' not in data:
                data['members'] = {}  # initializes 'members' if it's missing
            if target_id_str not in data['members']:
                data['members'][target_id_str] = {}

            data['members'][target_id_str]['gag'] = select.values[0]

        except Exception as e:  # Catches any errors during data manipulation
            print(f"Error updating gag data: {e}")
            return False

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:  # Catches any errors during file writing
            print(f"Error writing to file: {e}")
            return False


class Gagging(discord.Cog):
    """Cog for gagging commands."""

    def __init__(self, bot):
        """Initializes the gagging cog."""
        self.bot = bot

    gag = discord.SlashCommandGroup('gag', 'A place for all your gag needs', nsfw=True)

    @gag.command(name='equip', context='guild', description='This gives you a list of possible ways to gag a target')
    async def equipgag(self,
                       ctx: discord.ApplicationContext,
                       target: discord.Option(discord.User, name='subject', description='Who do you want to gag',
                                              required=True)):
        """Presents a select menu to choose a gag type for the target user.

        Args:
            ctx: The application context.
            target: The target user.
        """

        embed = discord.Embed(colour=discord.Colour.blue(), title='Gag')
        embed.add_field(name='Target', value=f'<@{target.id}>')
        view = GagTypes(target=target, timeout=30, author=ctx.author, response_gag=None, guild=ctx.guild.id,
                        interaction=ctx)
        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    """Loads the gagging cog."""
    bot.add_cog(Gagging(bot))
