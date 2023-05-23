import discord
from discord.ext import commands
from discord import app_commands
import data

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data = data.Data()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util cog loaded")

    #Dms are assumed to be elevenlabs keys
    @commands.Cog.listener("on_message")
    async def register_dm(self, message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            self.data.save_eleven_labs_key(message.author.id, message.content)
            await message.channel.send("Hello " + message.author.name + ", your elevenlabs id has been added")

    #Add <discord user name> + <elevenlabs id> to database
    # @app_commands.command(name="elevenlabs_register", description="Enter your ElevenLabs API Key")
    # async def register(self, interaction: discord.Interaction, id: str):
    #     message = "Congrats " + interaction.user.name + " your key has been registered!!!"
    #     await interaction.response.send_message(content=message)

async def setup(bot: commands.Bot):
    #await bot.add_cog(Util(bot))
    await bot.add_cog(Util(bot), guilds= [discord.Object(id=1089421585347248189)])