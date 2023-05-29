import time
import asyncio

import discord
from discord.ext import commands
from discord import app_commands

from elevenlabs import generate, save, voices

from EdgeGPT import Chatbot, ConversationStyle
import re

import helpers.data as data
import helpers.speech_api as speech_api 

"""
The Speech class is the heart of TTSBot, it utilizes the ElevenLabs API to produce AI-generated speech. 
"""


class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vc = None
        self.data = data.Data()
        self.speech_api = speech_api.Speech_API()

    @app_commands.command(
        name="leave_voice",
        description="Remove the bot from its current voice channel",
    )
    async def leave_voice(self, interaction: discord.Interaction):
        bot_voice_state = discord.utils.get(
            self.bot.voice_clients, guild=interaction.guild
        )
        if bot_voice_state:
            await bot_voice_state.disconnect()
            await interaction.response.send_message("Bye bye :)")
            return
        await interaction.response.send_message(
            "I'm not in a voice channel, Dingus",
            delete_after=120.0
        )

    # Returns true if successfully joined voice, false if joining failed or is not possible
    async def join_voice(self, interaction: discord.Interaction):
        user_voice_state = interaction.user.voice
        bot_voice_state = discord.utils.get(
            self.bot.voice_clients, guild=interaction.guild
        )

        # Check user status
        if user_voice_state == None:
            await interaction.response.send_message(
                content="My man, You have to join a voice channel before you can use me, Dingus",
                delete_after=120.0
            )
            return False

        # Check bot status
        if bot_voice_state == None:
            self.vc = await user_voice_state.channel.connect()
        elif user_voice_state.channel != bot_voice_state.channel:
            await bot_voice_state.disconnect()
            self.vc = await user_voice_state.channel.connect()

        return True

    async def play_audio(self):
        self.vc.play(discord.FFmpegPCMAudio(source=speech_api.AUDIO_FILE))
        while self.vc.is_playing():
            time.sleep(0.1)

    # Too many Azure Speech voices for this to be doable for Azure Speech
    def get_elevenlabs_voices():
        voice_list = []
        for voice in voices():
            voice_list.append(
                app_commands.Choice(name=voice.name, value=voice.name)
            )
        return voice_list
    
    async def speak(self,
        interaction: discord.Interaction,
        params = [],
        api_name="None"
        ):
        
        await interaction.response.send_message(
            content="Talking my shit",
            delete_after=5.0
            )
        
        # Speak
        try:
            await self.speech_api.api_call_dict[api_name](*params)
            await self.play_audio()
        except:
            await interaction.followup.send(
            content=api_name + " API Unavailable"
            )
            
    
    async def chatgpt_gen_response(self, prompt="Hello world"):
        # Sets regex pattern to remove emoji and other unwanted characters
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            "]+",
            flags=re.UNICODE
            )
        
        bot = await Chatbot.create() # Passing cookies is optional
        msg = await bot.ask(prompt=prompt + ". Answer in 100 words or fewer.", conversation_style=ConversationStyle.creative)
        out = msg['item']['messages'][1]['text'] # ToDo find a better way to access this info
        
        await bot.close()
        return emoji_pattern.sub(r'', out)

    # Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_eleven", description="Generate speech with ElevenLabs API")
    @app_commands.choices(voices=get_elevenlabs_voices())
    async def tts_eleven(
        self,
        interaction: discord.Interaction,
        voices: app_commands.Choice[str],
        unstable: bool,
        msg: str,
    ):
        # Join the proper voice channel
        if not await self.join_voice(interaction):
            return

        # Check is user is registered with appropriate key
        registered, key = self.data.get_eleven_labs_key(interaction.user.id)
        if not registered:
            await interaction.response.send_message(
                content="You're not registered\n"
                + "Register by sending me a DM of your elevenlabs xi-api-key https://api.elevenlabs.io/docs",
                ephemeral = True,
                delete_after=120.0
            )
            return

        # Speak
        params = [msg, key, voices.value, unstable]
        await self.speak(interaction=interaction, params=params, api_name="ElevenLabs",)

    # Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_azure", description="Generate speech with Azure API")
    @app_commands.choices(voices=[
        app_commands.Choice(name="Yunjian - Excited Chinese Sportscaster Male", value="zh-CN-YunjianNeural"),
        app_commands.Choice(name="Davis - African American Male", value="en-US-DavisNeural"),
        app_commands.Choice(name="Guy - White American Male", value="en-US-GuyNeural"),
        app_commands.Choice(name="Tony - White American Male", value="en-US-TonyNeural"),
        app_commands.Choice(name="Jason - Nerdy White American Male", value="en-US-JasonNeural"),
        app_commands.Choice(name="Jenny - White American Female", value="en-US-JennyNeural"),
        app_commands.Choice(name="Aria - White American Female", value="en-US-AriaNeural"),
        app_commands.Choice(name="Nancy - White American Female", value="en-US-NancyNeural"),
        app_commands.Choice(name="Sara - White American Female", value="en-US-SaraNeural"),
        app_commands.Choice(name="Jane - Educated White American Female", value="en-US-JaneNeural")
        ])
    @app_commands.choices(emotions=[
        app_commands.Choice(name="Default", value="default"),
        app_commands.Choice(name="Whispering", value="whispering"),
        app_commands.Choice(name="Shouting", value="shouting"),
        app_commands.Choice(name="Excited", value="excited"),
        app_commands.Choice(name="Cheerful", value="cheerful"),
        app_commands.Choice(name="Angry", value="angry"),
        app_commands.Choice(name="Unfriendly", value="unfriendly"),
        app_commands.Choice(name="Terrified", value="terrified"),
        app_commands.Choice(name="Sad", value="sad")
        ])
    async def tts_azure(self,
        interaction: discord.Interaction,
        voices: app_commands.Choice[str],
        emotions: app_commands.Choice[str],
        msg: str
    ):
        # Join the proper voice channel
        if not await self.join_voice(interaction):
            return
        
        # Speak
        params = [voices.value[:5], voices.value, emotions.value, msg]
        await self.speak(interaction=interaction, params=params, api_name="Azure")

    # Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_bing_chat", description="Generate speech with Azure API based on ChatGPT prompt")
    async def tts_bing_chat(self,
        interaction: discord.Interaction,
        msg: str
    ):
        # Join the proper voice channel
        if not await self.join_voice(interaction):
            return
        
        await interaction.response.send_message(
                content="You messaged me: " + msg
        )

        # Generate Bing response
        try:
            response = await self.chatgpt_gen_response(prompt=msg)
        except:
            await interaction.followup.send(
                content="Bing API Unavailable",
            )
            return
        
        # Speak
        params = ["en-US", "en-US-DavisNeural", "default", response]
        await self.speak(interaction=interaction, params=params, api_name="Azure")
            
    # Convert user-typed text into AI-generated speech
    @app_commands.command(name="tts_normal", description="Generate speech with some API")
    @app_commands.choices(voices=[app_commands.Choice(name="Man", value="Man")])
    async def tts_normal(
        self,
        interaction: discord.Interaction,
        voices: app_commands.Choice[str],
        msg: str
    ):
        # Join the proper voice channel
        if not await self.join_voice(interaction):
            return
        
        api_worked = await self.speech_api.choose_api(text=msg)
        if api_worked:
            await interaction.response.send_message(
                content="Talking my shit",
                delete_after=5.0
            )
            await(self.play_audio())
        else:
            await interaction.response.send_message(
            content="No API available",
            delete_after=5.0
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Speech(bot))
