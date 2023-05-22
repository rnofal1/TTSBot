import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from cogs import *

#Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Define client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

#on_ready() is called once the bot is booted up and a connection is established with a server
@client.event
async def on_ready():
    #Display the name of the connected server
    for guild in client.guilds:
        if guild.name == GUILD:
            print(
                f'{client.user} is connected to the following guild:'
                f'{guild.name}(id: {guild.id})\n'
            )
            break
    
cog_list = []
#Search for and load our cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_list.append("cogs." + filename[:-3])

# @tree.command(name = "elevenlabs_register", description = "Enter your ElevenLabs xi-api-key", guild=discord.Object(id=1089421585347248189)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
# async def elevenlabs_register(interaction):
#     user_name = interaction.user.id
#     await interaction.response.send_message("Congrats " + user_name + " your key has been registered")


client.run(TOKEN)