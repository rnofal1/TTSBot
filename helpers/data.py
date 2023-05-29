import pickle
import os.path
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

ELEVENLABS_KEY_FILE = "eleven_labs_keys.pkl"
AZURE_SSML_FILE = "helpers/ssml.xml"


class Data:
    def __init__(self):
        if not os.path.isfile(AZURE_SSML_FILE):
            self.write_azure_ssml_xml()

    def open_pickle(self):
        if os.path.isfile(ELEVENLABS_KEY_FILE):
            with open(ELEVENLABS_KEY_FILE, "rb") as file:
                return pickle.load(file)
        else:
            return {}

    def save_eleven_labs_key(self, user_id, key):
        eleven_labs_key_dict = self.open_pickle()

        eleven_labs_key_dict[user_id] = key

        with open(ELEVENLABS_KEY_FILE, "wb") as file:
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
    
    # NOTE: this function was generated primarily by ChatGPT
    def create_azure_ssml_xml_file(self):
        # Create the root element
        root = ET.Element("speak")
        root.set("version", "1.0")
        root.set("xmlns", "http://www.w3.org/2001/10/synthesis")
        ET.indent(root)
        ET.indent(root)
        root.set("xmlns:mstts", "https://www.w3.org/2001/mstts")
        root.set("xml:lang", "zh-CN")
        ET.indent(root)

        # Create the voice element
        voice = ET.SubElement(root, "voice")
        voice.set("name", "zh-CN-YunjianNeural")
        ET.indent(root)

        # Create the express-as element
        express_as = ET.SubElement(voice, "mstts:express-as")
        express_as.set("style", "sports_commentary_excited")
        express_as.set("styledegree", "1")
        ET.indent(root)

        # Set the text content of the express-as element
        express_as.text = "And he rounds third base, what a great day to be a Mets fan!!!"
        ET.indent(root)

        # Create the XML tree
        tree = ET.ElementTree(root)

        # Write the tree to an XML file
        tree.write(AZURE_SSML_FILE, xml_declaration=False)

    def write_azure_ssml_xml(self, lang="en-US", voice="en-US-DavisNeural", style="default", text="I'm speechless"):
        ET.register_namespace('',"http://www.w3.org/2001/10/synthesis")
        ET.register_namespace('mstts',"https://www.w3.org/2001/mstts")

        tree = ET.parse(AZURE_SSML_FILE)
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
        tree.write(AZURE_SSML_FILE)
    