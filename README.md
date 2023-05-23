# TTSBot
### Description
This project is a Discord-based TTS bot which allows users to generate AI-created speech using simple text commands leveraging the ElevenLabs API.

---
### Using TTSBot
First Time Setup:
- Install Discord Python API: ```pip install discord.py```
- Install elevenlabs official python API wrapper: ```pip install elevenlabs```
- Install PyNaCl ```pip install PyNaCl```
- Install ffmpeg to python ```pip install ffmpeg```
- Install ffmpeg to environment ```apt install ffmpeg```

To Run:
- ``` python3 client.py ```

---
### Development Roadmap
Short-Term ToDo:
- Change the bot/client in main into a custom class inheriting from Bot
- Put XML function(s) into a seperate file (CHANGE TO PICKLE)
- Change how xml data is created and organized (CHANGE TO PICKLE)
- Change behavior of dm registering of elevenlabs id depending on if user is already registered
- Modify FFmpegPCMAudio (in tts_normal, etc.) to use bitstream instead of wav
- Change how user info (such as ElevenLabs keys) is stored
- Add logging https://discordpy.readthedocs.io/en/latest/logging.html
- Check if the slash command for register displays what someone enters 

Long-Term ToDo:
- Control TTSBot through voice commands
- Distinguish between different voices (e.g. if Bill asks TTSBot for something, TTSBot will do that thing using Bill's stored info)