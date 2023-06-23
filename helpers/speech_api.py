# Standard
import os

# 3rd-party
import azure.cognitiveservices.speech as speechsdk
from elevenlabs import generate, save, voices, set_api_key, get_api_key

# Local
import helpers.data as data

# Defines
AUDIO_FILE = "temp_audio.wav"


# Within the Speech_API class, speech generation ends at saving the proper audio file
class Speech_API():
    def __init__(self):
        self.api_call_dict = {"ElevenLabs" : self.speak_eleven, "Azure" : self.speak_azure}
        self.data = data.Data()
    
    # Return True if audio was generated successfully, False otherwise
    async def choose_api(self, text="I'm speechless"):
        for api_name, api_call in self.api_call_dict.items():
            try:
                await api_call(msg=text)
                return True
            except:
                print(
                   api_name 
                   + " API not available"
                )
                continue
        return False
        
    async def speak_eleven(
        self, msg="I'm speechless", key=None, my_voice="Josh", unstable=False
    ):
        # Extract the actual voice object (this lets us modify the voice)
        voice_list = voices()
        voice_obj = voice_list[0]
        for voice in voices():
            if voice.name == my_voice:
                voice_obj = voice

        # Make it wacky if so desired
        if unstable:
            voice_obj.settings.stability = 0.05
            voice_obj.settings.similarity_boost = 0.09
        
        audio = generate(
            text=msg,
            #api_key=key,
            voice=voice_obj,
            model="eleven_monolingual_v1",
        )

        save(audio, AUDIO_FILE)

    async def speak_azure(self, lang="en-US", voice="en-US-DavisNeural", style="default",  msg="I'm speechless"):
        # Modify speech characteristics
        if voice == "zh-CN-YunjianNeural":
            style = "sports_commentary_excited"
        self.data.write_azure_ssml_xml(lang=lang, voice=voice, style=style, text=msg)

        # Create speech objects
        speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SPEECH_KEY"), region=os.getenv("SPEECH_REGION"))
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        file_config = speechsdk.audio.AudioOutputConfig(filename=AUDIO_FILE)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

        # Synthesize speech
        ssml_string = open(data.AZURE_SSML_FILE, "r").read()
        result = speech_synthesizer.speak_ssml_async(ssml_string).get()
        