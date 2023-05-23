import pickle
import os.path

#Primarily handles user info
class Data():
    def __init__(self):
        self.key_filename = 'eleven_labs_keys' + '.pkl'
    
    def open_pickle(self):
        if os.path.isfile(self.key_filename):
            with open(self.key_filename, 'rb') as file:
                return pickle.load(file)
        else:
            return {}
        
    def save_eleven_labs_key(self, user_id, key):
        eleven_labs_key_dict = self.open_pickle()

        eleven_labs_key_dict[user_id] = key

        with open(self.key_filename, 'wb') as file:
            pickle.dump(eleven_labs_key_dict, file)

    """
    If user is registered, returns tuple (True, key associated with the user)
    If user is  not registered, returns tuple (False, None)
    """
    def get_eleven_labs_key(self, user_id):
        eleven_labs_key_dict = self.open_pickle()
        if user_id in eleven_labs_key_dict:
            return True, eleven_labs_key_dict[user_id]
        else:
            return False, None 


