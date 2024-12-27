import discord


class Latency(discord.Cog):
    """Cog for measuring and displaying bot latency."""

    def __init__(self, bot):
        """Initializes the cog with the bot instance."""
        self.bot = bot

    @discord.slash_command(description="Sends the latency of the bot", name="ping")
    async def latency_cmd(self, ctx: discord.ApplicationContext):
        """
        Slash command to measure and respond with the bot's latency.

        Args:
            ctx: The application context.
        """
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blue(), title="Pong!",
                              description=f"The latency is {latency_ms}ms")
        await ctx.respond(embed=embed)
        print(f"{latency_ms}ms")


def setup(bot):
    """Loads the cog."""
    bot.add_cog(Latency(bot))