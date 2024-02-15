import json, os

class SettingsDTO():
    def __init__(self):        
        self.json_dict = self.charge_json()

    def charge_json(self):
        settings_file_path = os.path.join('settings.json')
        with open(settings_file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    
    def modified_json(self, new_initial, new_algorithm, new_depth):
        self.json_dict['initial'] = new_initial
        self.json_dict['algorithm'] = new_algorithm
        self.json_dict['depht'] = new_depth
        
        settings_file_path = os.path.join('settings.json')
        with open(settings_file_path, 'w') as json_file:
            json.dump(self.json_dict, json_file, indent=4)
