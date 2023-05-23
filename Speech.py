from discord.ext import commands

class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #Convert user-typed text into AI-generated speech
    def tts_normal(self):
        pass

    #Convert randomly-found text into AI-generated speech
    def tts_ramble(self):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Speech(bot))
    