# Standard
import os.path
import xml.etree.ElementTree as ET
import pickle
from dotenv import load_dotenv

# Defines
ELEVENLABS_USER_FILE = "eleven_labs_users.pkl"
AZURE_SSML_FILE = "helpers/ssml.xml"
ELEVENLABS_CHAR_ALLOC = 2000 # Number of characters for new ElevenLabs users


class Data:
    def __init__(self):
        if not os.path.isfile(AZURE_SSML_FILE):
            self.create_azure_ssml_xml_file()

    def open_pickle(self):
        if os.path.isfile(ELEVENLABS_USER_FILE):
            with open(ELEVENLABS_USER_FILE, "rb") as file:
                return pickle.load(file)
        else:
            return {}

    def save_pickle(self, dict):
        with open(ELEVENLABS_USER_FILE, "wb") as file:
            pickle.dump(dict, file)

    # Return number of characters remaining for user; register user if not already registered
    def get_elevenlabs_allocation(self, user_id, user_name):
        eleven_labs_user_dict = self.open_pickle()

        if user_id in eleven_labs_user_dict:
            return eleven_labs_user_dict[user_id][0]

        eleven_labs_user_dict[user_id] = ELEVENLABS_CHAR_ALLOC, user_name

        self.save_pickle(eleven_labs_user_dict)

        return ELEVENLABS_CHAR_ALLOC

    # ToDo: make this more robust to misuse (e.g. if this is called before get_elevenlabs_allocation)
    def update_elevenlabs_allocation(self, user_id, user_name, num_chars):
        eleven_labs_user_dict = self.open_pickle()

        if user_id in eleven_labs_user_dict:
            eleven_labs_user_dict[user_id] = eleven_labs_user_dict[user_id][0] - num_chars, eleven_labs_user_dict[user_id][1]
        else:
            eleven_labs_user_dict[user_id] = ELEVENLABS_CHAR_ALLOC - num_chars, user_name
        
        self.save_pickle(eleven_labs_user_dict)

    # Requires: user_id exists in the dict of ElevenLabs character allocations
    def set_elevenlabs_allocation(self, user_id, num_chars):
        eleven_labs_user_dict = self.open_pickle()

        if user_id in eleven_labs_user_dict:
            print("Previous allocation: " + str(eleven_labs_user_dict[user_id]))
            eleven_labs_user_dict[user_id] = num_chars, eleven_labs_user_dict[user_id][1]
            print("Updated allocation: " + str(eleven_labs_user_dict[user_id]))
            self.save_pickle(eleven_labs_user_dict)
        else:
            print(f"User ID {user_id} not found")

    # Requires: user_id exists in the dict of ElevenLabs character allocations
    def reset_elevenlabs_allocation(self, user_id):
        self.set_elevenlabs_allocation(user_id=user_id, num_chars=ELEVENLABS_CHAR_ALLOC)

    # Requires: user_id exists in the dict of ElevenLabs character allocations
    def add_to_elevenlabs_allocation(self, user_id, num_chars):
        eleven_labs_user_dict = self.open_pickle()

        if user_id in eleven_labs_user_dict:
            print("Previous allocation: " + str(eleven_labs_user_dict[user_id]))
            eleven_labs_user_dict[user_id] = eleven_labs_user_dict[user_id][0] + num_chars, eleven_labs_user_dict[user_id][1]
            print("Updated allocation: " + str(eleven_labs_user_dict[user_id]))
            self.save_pickle(eleven_labs_user_dict)
        else:
            print(f"User ID {user_id} not found")

    # Requires: user_id exists in the dict of ElevenLabs character allocations
    def subtract_from_elevenlabs_allocation(self, user_id, num_chars):
        self.add_to_elevenlabs_allocation(user_id=user_id, num_chars=-num_chars)

    """
    For full description of SSML document structure:
    https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup-structure
    """
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
    