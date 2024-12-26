#importing needed libs
import discord
import json

#Here i put the file locations
guilds_file= 'Database/Guilds.json'

#Here I put the API key
with open("API_Keys.json","r") as API_file:
    data = json.load(API_file)
    Api_Key_DiscordBot= data["discord"]


#Here i put the guilds file
guilds_file= 'Database/Guilds.json'

#importing needed libs
import discord
import json

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

    in_guilds_id = []
    print(f'the bot is in folowing guilds')
    for guild in bot.guilds:
        in_guilds_id.append(guild.id)
        if guild.id not in data_id:
            data_id.append(guild.id)
            try:
                file = open(f'Database/Guilds/{guild.id}.json', 'x')
                file.write(' ')
                file.close()
            except:
                pass

    print(in_guilds_id)

    with open(guilds_file, 'w') as jsonFile:
        json.dump(data, jsonFile)


#this adds all the cogs to the bot
def start_cogs():
    #this is a list off all the cogs
    cogs_list = [
        'ping'
    ]
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')

#This actually starts up the bot
#To the person that leaks the api key
#I will and come and hunt you in your sleep
start_cogs()
bot.run(Api_Key_Discordbot)