from ..LLMInterface import LLMInterface
from ..LLMsEnum import OPENAIEnum
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
    
    def __init__(self,api_key:str, api_url:str=None,default_input_max_length:int=1000,default_output_max_tokens:int=1000,default_temperature:float=0.5):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_length = default_input_max_length
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key=api_key,base_url=api_url)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id:str):
        self.generation_model_id = model_id

       
    def set_embedding_model(self, model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text:str):
        return text[:self.default_input_max_length].strip()
    
    def generate_text(self, prompt:str,chat_history:list=[], max_length:int=None, temperature:float=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model is not set")
            return None
        max_length = max_length if max_length else self.default_output_max_tokens
        temperature = temperature if temperature else self.default_temperature
        
        chat_history.append(self.construct_prompt(prompt, OPENAIEnum.USER.value))
        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_length,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("failed to generate text")
            return None
        return response.choices[0].message["content"]
    
    def embed_text(self, text:str, document_type:str=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set")
            return None
        response = self.client.embeddings.create(model=self.embedding_model_id, input=text)
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("failed to embed text")
            return None
        return response.data[0].embedding

    
    def construct_prompt(self, prompt:str, role:str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }