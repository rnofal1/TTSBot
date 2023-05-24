import time

import discord
from discord.ext import commands
from discord import app_commands

from elevenlabs import generate, save, voices

import data

"""
The Speech class is the heart of TTSBot, it utilizes the ElevenLabs API to produce AI-generated speech. 
"""
class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vc = None
        self.data = data.Data()

    @app_commands.command(name="leave_voice", description="Remove the bot from its current voice channel")
    async def leave_voice(self, interaction: discord.Interaction):
        bot_voice_state = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if bot_voice_state:
            await bot_voice_state.disconnect()
            await interaction.response.send_message("Bye bye :)")
            return
        await interaction.response.send_message("I'm not in a voice channel, Dingus")

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
            await bot_voice_state.disconnect()
            self.vc = await user_voice_state.channel.connect()

        return True
            
    def speak(self, msg="I'm speechless", key=None, my_voice='Josh', unstable=False):
        #Extract the actual voice object (this lets us modify the voice)
        voice_list = voices()
        voice_obj = voice_list[0]
        for voice in voices():
            if voice.name == my_voice:
                voice_obj = voice

        #Make it wacky if so desired
        if unstable:
            voice_obj.settings.stability = 0.05
            voice_obj.settings.similarity_boost = 0.09

        audio = generate(
            text=msg,
            api_key=key,
            voice=voice_obj,
            model="eleven_monolingual_v1"
        )
        save(audio, 'temp_audio.wav')
       
        self.vc.play(discord.FFmpegPCMAudio(source="temp_audio.wav"))
        while self.vc.is_playing():
            time.sleep(.1)

    def get_voices():
        voice_list = []
        for voice in voices():
            voice_list.append(app_commands.Choice(name=voice.name, value=voice.name))
        return voice_list
    
    #Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_normal", description="Generate Speech")
    @app_commands.choices(voices=get_voices())
    async def tts_normal(self, interaction: discord.Interaction, voices: app_commands.Choice[str], unstable: bool, msg: str):
        #Join the proper voice channel
        joined_voice = await self.join_voice(interaction)
        if not joined_voice:
            await interaction.response.send_message(content="You have to join a voice channel before you can use me, Dingus")
            return
        
        #Check is user is registered with appropriate key
        registered, key = self.data.get_eleven_labs_key(interaction.user.id)
        if not registered:
            await interaction.response.send_message(content="You're not registered\n" 
                + "Register by sending me a DM of your elevenlabs xi-api-key https://api.elevenlabs.io/docs")
            return
        
        #Speak
        await interaction.response.send_message(content="Talking my shit")
        self.speak(msg=msg, key=key, my_voice=voices.value, unstable=unstable)
        await interaction.followup.send("There, I said it")

async def setup(bot: commands.Bot):
    await bot.add_cog(Speech(bot))
    