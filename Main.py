# Importing necessary libraries
from typing import Any
import discord
import json

# File locations
guilds_file = f'Database/Guilds.json'

# API Key retrieval
with open("API_Keys.json", "r") as API_file:
    data = json.load(API_file)
    Api_Key_DiscordBot = data["discord"]

# Define bot intents (permissions)
# Important for bots in 100+ servers (requires verification)
intents = discord.Intents.all()

# Create bot instance
bot = discord.Bot(intents=intents)


# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print('-----')
    print(f"Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

    # Load guild data
    try:
        with open(guilds_file, "r") as jsonFile:
            data = json.load(jsonFile)
        data_id = data['ids']
    except:
        print(f'Error loading the guild list')
        quit()


    # Initialize list of guild IDs the bot is currently in
    global in_guilds_id
    in_guilds_id = []
    print(f'The bot is in the following guilds:')

    # Iterate through guilds the bot is in
    for guild in bot.guilds:
        in_guilds_id.append(guild.id)
        # Check if guild is already in the database
        if guild.id not in data_id:
            # Add new guild to the database
            data_id.append(guild.id)
            print(f"Adding new guild: {guild.id}")  # Indicate new guild added

            # Create a new file for the guild
            try:  # Added error handling in case file creation fails.
                with open(f'Database/Guilds/{guild.id}.json', 'x') as MemberFile:  # 'x' mode for exclusive creation
                    pass  # File created, nothing more to do here. 'x' mode ensures no overwrite.
            except FileExistsError:  # Handle the case where file already exists.
                print(f"Database file for guild {guild.id} already exists.")

            # Initialize member data for the guild
            member_data = {"members": {}}
            with open(f'Database/Guilds/{guild.id}.json', 'w') as MemberFile:  # 'w' mode to write data.
                memberdic = member_data["members"]
                members = guild.fetch_members()
                async for member in members:
                    memberdic[member.id] = {"gag": {"type":None, "effect":None}, "owner": None,
                                            "restrains": {'arms': None, 'legs': None, 'neck': None,
                                                          'hands': None, 'head': None,
                                                          'suit': None, 'genitals': None}, "locked": None,
                                            "needtotalk": False}
                json.dump(member_data, MemberFile, indent=4)  # Added indent for readability

    print(in_guilds_id)

    # Save updated guild data
    try:
        with open(guilds_file, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)  # Added indent for readability
    except:
        print(f'Error saving the guild list')
        quit()


# Function to load cogs (extensions)
def start_cogs():
    cogs_list = {
        'ping',
        'status',
        'gag'
    }
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')


# Start the bot
start_cogs()
print(bot.extensions)
bot.run(Api_Key_DiscordBot)