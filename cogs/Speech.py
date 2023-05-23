import discord
from discord.ext import commands
from discord import app_commands, FFmpegPCMAudio, PCMAudio
import xml.etree.ElementTree as ET
from elevenlabs import generate, play, set_api_key, save
import time
import io

class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vc = None

    async def leave_voice(self, interaction: discord.Interaction):
        bot_voice_state = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if bot_voice_state:
            await bot_voice_state.disconnect()

    #Returns true if successfully joined voice, false if joining failed or is not possible
    async def join_voice(self, interaction: discord.Interaction):
        user_voice_state = interaction.user.voice
        bot_voice_state = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        #Check user status
        if user_voice_state == None:
            return False

        #Check bot status
        if bot_voice_state == None:
            self.vc = await user_voice_state.channel.connect()
        elif user_voice_state.channel != bot_voice_state.channel:
            await bot_voice_state.move_to(user_voice_state.channel)

        return True
            

    #Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_normal", description="Generate Speech")
    async def tts_normal(self, interaction: discord.Interaction, msg:str):
        #Join the proper voice channel
        joined_voice = await self.join_voice(interaction)
        if not joined_voice:
            await interaction.response.send_message(content="You have to join a voice channel before you can use me, Dingus")
            return
        
        #Speak
        await interaction.response.send_message(content="Talking my shit")
        set_api_key("f207a84adb56ae273a602d7b8e330914")
        print("!!!")
        audio = generate(
            text="A",
            voice="Bella",
            model="eleven_monolingual_v1"
        )
        print("!!!")
        #save(audio, 'example.wav')
        print("!!!")
        #self.vc.play(discord.FFmpegPCMAudio(source="example.wav"))
        self.vc.play(discord.FFmpegPCMAudio(io.BufferedIOBase(audio)))
        while self.vc.is_playing():
            time.sleep(.1)
        await interaction.followup.send("There, I said it")

    #Convert randomly-found text into AI-generated speech
    def tts_ramble(self):
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(Speech(bot), guilds= [discord.Object(id=1089421585347248189)])
    