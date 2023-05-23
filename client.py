import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from cogs import *

#Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Define client
intents = discord.Intents.default()
client = commands.Bot(command_prefix='?', intents=intents)

#Output a ready message
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
    await sync_tree(guild)

#Load cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await client.load_extension("cogs." + filename[:-3])
    print("Extensions Loaded")

#Sync tree
async def sync_tree(guild):
    client.tree.copy_global_to(guild=guild)
    await client.tree.sync(guild=guild)
    await client.tree.sync()
    print("Tree synced")

async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())

# import discord
# from discord.ext import commands

# class MyBot(commands.Bot):
#     def __init__(self):
#         super().__init__(
#             command_prefix='$',
#             intents=discord.Intents.all(),
#             application_id = 1089419303402606592)
        
#     async def setup_hook(self):
#         await self.load_extension(f"cogs.Util")
#         await bot.tree.sync(guild=discord.Object(id=1089421585347248189))

#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')

# bot = MyBot()
# bot.run('MTA4OTQxOTMwMzQwMjYwNjU5Mg.GemOVW.SZUW7hGUvhpJChrYxU35UedaA2yiKekCJvc5I4')