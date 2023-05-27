from discord.ext import commands

import helpers.data as data


class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data = data.Data()

    # DMs are assumed to be ElevenLabs keys
    @commands.Cog.listener("on_message")
    async def register_dm(self, message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            self.data.save_eleven_labs_key(message.author.id, message.content)
            await message.channel.send(
                f"Hello {message.author.name}, your ElevenLabs ID has been added."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Util(bot))
