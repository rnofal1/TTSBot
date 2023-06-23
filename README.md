# TTSBot
### Description  
This project is a Discord-based Text-to-Speech (TTS) bot which allows users to play AI-generated speech within a voice channel using simple text commands.  

This project leverages several APIs, development kits, and libraries:  
ElevenLabs API
- https://api.elevenlabs.io/docs
- https://github.com/elevenlabs/elevenlabs-python

Microsoft Azure Speech SDK
- https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-sdk
- https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup-voice  

Reverse-engineered Bing Chat API
- https://github.com/acheong08/EdgeGPT  

---
### Using TTSBot
Registration (Optional) :  
- To use ElevenLabs speech generation, a user must first register their ElevenLabs API key with TTSBot by sending a direct message to TTSBot containing only their ElevenLabs API key (Create an ElevenLabs account at https://beta.elevenlabs.io/sign-up &rarr; Go to https://beta.elevenlabs.io/ &rarr; Click on top right profile picture &rarr; ```Profile``` &rarr; ```API Key```)
- This is necessary since ElevenLabs only provides a limited number of characters per user for speech generation  

TTS:  
TTSBot features several different TTS commands to leverage a host of available speech-generation APIs:
- ```/tts_azure``` Generates speech using the Azure Speech SDK
    - The ```voices``` field lets the user select from the available Azure voices
    - The ```emotions``` field lets the user choose from a selection of speaking styles
    - The ```msg``` field is where the user enters the actual content to be spoken by TTSBot  
&nbsp;  

- ```/tts_eleven``` Generates speech using the ElevenLabs API
    - The ```voices``` field lets the user select from the available ElevenLabs voices
    - The ```unstable``` field lets the user choose whether to make the speech "normal" (```false```) or unstable/wacky/unpredictable (```true```)
    - The ```msg``` field is where the user enters the actual content to be spoken by TTSBot  
&nbsp;  

- ```/tts_normal``` Cycles through the available APIs until TTSBot successfully generates speech (helpful since many APIs have character limits on speech generation)
    - The ```voices``` field lets the user select from either a ```Male``` or ```Female``` voice
    - The ```msg``` field is where the user enters the actual content to be spoken by TTSBot  
&nbsp;

- ```/tts_bing_chat``` Lets the user converse with Bing Chat. Responses are spoken back through Azure TTS
    - The ```msg``` field is where the user enters the prompt which is sent to Bing Chat  
&nbsp;

- Sending a TTS command will move TTSBot into the user's voice channel, where TTSBot will begin speaking
- After speaking, TTSBot will remain in the voice channel

Misc - Leave:
- ```/leave_voice``` lets the user evict TTSBot from its voice channel

---
### Hosting TTSBot
First Time Setup:
- Install basic Python requirements ```pip install -r requirements.txt```
- Install ffmpeg to environment ```apt install ffmpeg```
- Rename the file ```.env_example``` to ```.env``` after filling out the following fields:  
     1. ```DISCORD_TOKEN``` | Discord Bot Token (from the Discord developer site)
     2. ```DISCORD_GUILD``` | Discord Guild Name (where you will use the bot)
     3. ```SPEECH_KEY```    | Azure Speech Key
     4. ```SPEECH_REGION``` | Azure Speech Region
     5. ```BARD_QUICK```    | Bard Quick Response Preference
     6. ```BARD_SESSION```    | Bard Session Key (see EdgeGPT setup description)
     7. ```OPENAI_API_KEY```    | OpenAI API Key (currently optional)
     8. ```ELEVENLABS_KEY```    | ElevenLabs API Key
     9. ```ADMIN_USER_ID```    | Discord User ID for Primary Bot Admin (e.g. your user id)

To Run:
- ``` python3 client.py ```

---
### Development Roadmap
Short-Term ToDo:
- Reorganize Util and Speech classes for comprehensibility
- Modify FFmpegPCMAudio (in tts_normal, etc.) to use bitstream instead of wav
- Improve logging
- Implement robust error handling
- Conduct comprehensive unit tests
- Generally reorganize dependancy handling and code format to be more comprehensible and robust

Long-Term ToDo:
- Switch from Bing Chat to ChatGPT
- Implement "One-shot" voice cloning using ElevenLabs API or Azure Speech 
- Control TTSBot through voice commands
- Distinguish between different voices (e.g. if Bill asks TTSBot for something, TTSBot will do that thing using Bill's stored info)

Extremely Long-Term ToDo:
- Transition to a locally-run model
- Implement "Deep" voice cloning with local training