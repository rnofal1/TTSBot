# TTSBot
### Description
This project is a Discord-based TTS bot which allows users to generate AI-created speech using simple text commands leveraging the ElevenLabs API.

---
### Using TTSBot
First Time Setup:
- Install Discord Python API: ```pip install discord.py```
- Install elevenlabs official python API wrapper: ```pip install elevenlabs```

To Run:
- ``` python3 client.py ```

---
### Development Roadmap
Short-Term ToDo:
- Put XML stuff into a seperate file
- Change behavior of dm registering of elevenlabs id depending on if user is already registered
- Change how xml data is created and organized
- Change how user info (such as ElevenLabs keys) is stored
- Add logging https://discordpy.readthedocs.io/en/latest/logging.html 

Long-Term ToDo:
- Control TTSBot through voice commands
- Distinguish between different voices (e.g. if Bill asks TTSBot for something, TTSBot will do that thing using Bill's stored info)