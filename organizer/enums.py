"""
Copyright 2024 Smarg1

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from enum import Enum

class Settings:
    def __load_enums(self):
        """
        Load Settings File
        """
        with open("../settings.json", "r") as f:
            enums: dict = json.load(f)
        return enums
    
    def get_theme(self):
        tmp = self.__load_enums()
        current_gui = tmp["_settings"]["_gui"]["cur"]
        return tmp["_settings"]["_gui"][current_gui]
    
    def set_theme(self, theme):
        with open('settings.json', 'r') as f:
            data = json.load(f)

        data['_settings']['_gui']['cur'] = theme
        
        with open('settings.json', 'w') as f:
            json.dump(data, f, indent=4)

class enum(Enum):
    DATE = "date"
    SIZE = "size"
    APP = "app"
    TYPE = "type"
    @classmethod
    def __custom():
        pass
    
if __name__ == '__main__':
    pass