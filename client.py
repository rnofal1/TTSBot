# Standard
import os
import asyncio
from datetime import datetime

# 3rd-party
import discord
from discord.ext import commands
from elevenlabs import set_api_key, get_api_key
from loguru import logger

# Local
import helpers.data as data


class TTSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=discord.Intents.default())
        self.data = data.Data()
        self.set_env_vars()
        set_api_key(self.ELEVENLABS_KEY) # Sets elevenlabs key globally

    def set_env_vars(self):
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD_NAME = os.getenv("DISCORD_GUILD")
        self.ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")

        if not all([self.TOKEN, self.GUILD_NAME, self.ELEVENLABS_KEY]):
            print(
                "ERROR in .env file, double check format in top-level"
                " README.md"
            )
            exit()

    async def setup_hook(self):
        # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                await self.load_extension("cogs." + filename[:-3])
        print("Extensions loaded")

    # Sync tree
    async def sync_tree(self, guild):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("Tree synced")

    async def on_ready(self):
        # Display the name of the connected server
        for guild in self.guilds:
            if guild.name == self.GUILD_NAME:
                print(
                    f"{self.user} is connected to the following guild:"
                    f"{guild.name}(id: {guild.id})\n"
                )

                # Sync tree (for app commands)
                self.GUILD_OBJ = guild
                await self.sync_tree(guild)
                return

        # If not connected
        print("Something went wrong on startup...")
        exit()

async def log_start():
    date = str(datetime.now())[:10]
    logger.add("tts_requests_" + date + ".log",
        format="{time:YYYY-MM-DD at HH:mm:ss} "
        + "| {extra[user]} "
        + "| {extra[command]} "
        + "| {extra[voice]} "
        + "| {extra[emotion]} "
        + "| {message}\n"
    )
    

async def main():
    data.load_dotenv()
    await log_start()
    bot = TTSBot()
    async with bot:
        await bot.start(bot.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
