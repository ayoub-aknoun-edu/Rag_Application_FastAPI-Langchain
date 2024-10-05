from fastapi import Depends, UploadFile
from helpers.config import Settings, get_settings
from .BaseController import BaseController
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):


    def __init__(self):
        super().__init__()


    def validate_uploaded_file(self, file:UploadFile)->tuple:
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value   
        if file.size/1048576 > self.app_settings.FILE_MAX_SIZE: # 1024**2 bytes == 1048576 == 1MB 
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value


    def generate_unique_filepath(self, original_file_name:str, project_id:str)->str:
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(original_file_name)
        new_file_path = os.path.join(project_path, f"{random_filename}_{cleaned_file_name}")
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_filename}_{cleaned_file_name}")
        return new_file_path, f"{random_filename}_{cleaned_file_name}"


    def get_clean_file_name(self, file_name:str)->str:
        # leave only letters, numbers, dots and dashes
        cleaned_file_name = re.sub(r'[^\w.-]', '_', file_name.strip())

        # replace space with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        return cleaned_file_name

