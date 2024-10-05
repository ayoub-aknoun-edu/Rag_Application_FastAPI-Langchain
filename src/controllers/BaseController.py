from fastapi import Depends
from helpers.config import get_settings, Settings
import os
import random, string

class BaseController:

    def __init__(self):
        self.app_settings:Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        self.file_dir = os.path.join(self.base_dir , "assets/files")

        self.database_dir = os.path.join(self.base_dir , "assets/database")

    
    def generate_random_string(self, length:int=12)->str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    

    def get_database_path(self, db_name:str)->str:
        path = os.path.join(self.database_dir, db_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path