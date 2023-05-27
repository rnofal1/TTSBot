import pickle
import os.path
import xml.etree.ElementTree as ET
from dotenv import load_dotenv


# Primarily handles user info
class Data:
    def __init__(self):
        self.key_filename = "eleven_labs_keys" + ".pkl"

    def open_pickle(self):
        if os.path.isfile(self.key_filename):
            with open(self.key_filename, "rb") as file:
                return pickle.load(file)
        else:
            return {}

    def save_eleven_labs_key(self, user_id, key):
        eleven_labs_key_dict = self.open_pickle()

        eleven_labs_key_dict[user_id] = key

        with open(self.key_filename, "wb") as file:
            pickle.dump(eleven_labs_key_dict, file)

    """
    If user is registered, returns the tuple:
        (True, <key associated with the user>)
    If user is not registered, returns the tuple:
        (False, None)
    """

    def get_eleven_labs_key(self, user_id):
        eleven_labs_key_dict = self.open_pickle()
        if user_id in eleven_labs_key_dict:
            return True, eleven_labs_key_dict[user_id]
        else:
            return False, None

    def get_env_vars(self):
        load_dotenv()
        return os.getenv("DISCORD_TOKEN"), os.getenv("DISCORD_GUILD")
    
    def write_azure_ssml_xml(self, file_name="helpers/ssml.xml", lang="en-US", voice="en-US-DavisNeural", style="default", text="I'm speechless"):
        ET.register_namespace('',"http://www.w3.org/2001/10/synthesis")
        ET.register_namespace('mstts',"https://www.w3.org/2001/mstts")

        tree = ET.parse(file_name)
        speak = tree.getroot()

        #Set lang
        speak.set("{http://www.w3.org/XML/1998/namespace}lang", lang)

        #Set voice
        voice_node = speak.find("{http://www.w3.org/2001/10/synthesis}voice")
        voice_node.attrib['name'] = voice

        #Set style
        express_as = voice_node.find("{https://www.w3.org/2001/mstts}express-as")
        express_as.attrib['style'] = style
        
        #Set text
        express_as.text = text
        tree.write(file_name)
    