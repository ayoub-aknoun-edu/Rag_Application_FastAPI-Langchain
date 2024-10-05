from enum import Enum

class LLMsEnum(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    OLLAMA = "OLLAMA"

class OPENAIEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class COHEROEnum(Enum):
    SYSTEM = "SYSTEM"
    USER =  "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT= "search_document"
    QUERY = "search_query"

class DocumentTypeEnum(Enum):
    DOCUMENT= "document"
    QUERY = "query"