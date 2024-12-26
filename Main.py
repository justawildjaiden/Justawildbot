#importing needed libs
import discord
import json

#Here i put the file locations
guilds_file= f'Database/Guilds.json'

#Here I put the API key
with open("API_Keys.json","r") as API_file:
    data = json.load(API_file)
    Api_Key_DiscordBot= data["discord"]



#intents say what the bot can and cant do
#this is linked to the dev website
#once the bot gets in 100+ servers I need to verify i
intents = discord.Intents.all()


#here we specify what command sign we want to use,
#im planning on limiting this as much as possible to / commands
bot = discord.Bot()

#this runs once the bot has been booted
@bot.event
async def on_ready():

    print('-----')
    print(f"Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

    #open the guilds database
    with open(guilds_file, "r") as jsonFile:

        #convert the json to dic
        data = json.load(jsonFile)
    data_id = data['ids']

    global in_guilds_id
    in_guilds_id = []
    print(f'the bot is in folowing guilds')
    #updates the list the bot is in, and creates a database file for the guild
    for guild in bot.guilds:
        in_guilds_id.append(guild.id)
        if guild.id not in data_id:
            data_id.append(guild.id)

            #create file for the guild
            file = open(f'Database/Guilds/{guild.id}.json', 'w')
            file.close()
            member_data = {"members": {}}
            with open(f'Database/Guilds/{guild.id}.json', 'w') as MemberFile:
                memberdic = member_data["members"]
                members = guild.fetch_members()
                async for member in members:
                    memberdic[member.id] = {"gag": None, "owner": None,
                                            "restrains": {'arms': None, 'legs': None, 'neck': None,
                                                          'hands': None, 'head': None,
                                                          'suit': None, 'genitals': None}
                        , "locked": None}

                json.dump(member_data, MemberFile)
    print(in_guilds_id)

    with open(guilds_file, 'w') as jsonFile:
        json.dump(data, jsonFile)


#this adds all the cogs to the bot
def start_cogs():
    #this is a list off all the cogs
    cogs_list = [
        'ping',
        'owner'
    ]
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')

#This actually starts up the bot
#To the person that leaks the api key
#I will and come and hunt you in your sleep
start_cogs()
print(bot.extensions)
bot.run(Api_Key_DiscordBot)