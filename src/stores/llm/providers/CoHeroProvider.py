from ..LLMInterface import LLMInterface
from ..LLMsEnum import COHEROEnum, DocumentTypeEnum
import cohere
import logging

class CoHeroProvider(LLMInterface):

    def __init__(self,api_key:str, default_input_max_length:int=1000,default_output_max_tokens:int=1000,default_temperature:float=0.5):
        self.api_key = api_key

        self.default_input_max_length = default_input_max_length
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=api_key)

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
            self.logger.error("CoHere client is not initialized")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model is not set")
            return None
        
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message= self.process_text(prompt),
            temperature= temperature if temperature else self.default_temperature,
            max_tokens= max_length if max_length else self.default_output_max_tokens
        )

        if not response or not response.text:
            logging.error("failed to generate text with CoHere")
            return None
        return response.text
    
    def embed_text(self, text:str, document_type:str):
        if not self.client:
            self.logger.error("CoHere client is not initialized")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set")
            return None
        input_type = COHEROEnum.DOCUMENT.value if document_type == DocumentTypeEnum.DOCUMENT.value else COHEROEnum.QUERY.value
        response = self.client.embed(
            model= self.embedding_model_id,
            texts= [self.process_text(text)],
            input_type= input_type,
            embedding_types= ['float']
        )
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("failed to embed text with CoHere")
            return None
        return response.embeddings.float[0]

    def construct_prompt(self, prompt:str, role:str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }