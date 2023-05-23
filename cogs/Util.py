import discord
from discord.ext import commands
from discord import app_commands
import xml.etree.ElementTree as ET

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util cog loaded")

    @commands.Cog.listener("on_message")
    async def register_dm(self, message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            tree = ET.parse('eleven_labs_ids.xml')
            root = tree.getroot()

            found = False

            for user in root.findall('user'):
                if(user.get('name') == message.author.name):
                    user.attrib['id'] = message.content
                    found = True
            if not found:
                user = ET.Element("user", name=message.author.name, id=message.content)
                root.insert(0, user)
            tree.write('eleven_labs_ids.xml')
            
            await message.channel.send("Hello, " + message.author.name + " your elevenlabs id has been added")

    #Add <discord user name> + <elevenlabs id> to database
    @app_commands.command(name="elevenlabs_register", description="Enter your ElevenLabs API Key")
    async def register(self, interaction: discord.Interaction, id: str):
        message = "Congrats " + interaction.user.name + " your key has been registered!!!"
        await interaction.response.send_message(content=message)

async def setup(bot: commands.Bot):
    #await bot.add_cog(Util(bot))
    await bot.add_cog(Util(bot), guilds= [discord.Object(id=1089421585347248189)])

# import discord
# from discord import app_commands
# from discord.ext import commands

# class Util(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot

#     @app_commands.command(name="testingslash", description="testingslash")
#     async def testingslash(self, interaction:discord.Interaction):
#         await interaction.response.send_message("Congrats your key has been registered")

# async def setup(bot: commands.Bot):
#     await bot.add_cog(Util(bot), guilds = [discord.Object(id=1089421585347248189)])