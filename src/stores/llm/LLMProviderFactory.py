from .LLMsEnum import LLMsEnum
from .providers import OpenAIProvider, CoHeroProvider 
from helpers.config import Settings

class LLMProviderFactory:
    
    def __init__(self, config:Settings):
        self.config = config

    def create(self, provider:str):
        if provider == LLMsEnum.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_length = self.config.INPUT_DEFAULT_MAX_LENGTH,
                default_output_max_tokens= self.config.OUTPUT_DEFAULT_MAX_TOKENS,
                default_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        if provider == LLMsEnum.COHERE.value:
            return CoHeroProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_length= self.config.INPUT_DEFAULT_MAX_LENGTH,
                default_output_max_tokens= self.config.OUTPUT_DEFAULT_MAX_TOKENS,
                default_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        return None