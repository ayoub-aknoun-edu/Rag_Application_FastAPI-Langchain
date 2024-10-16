from .BaseController import BaseController
from models.db_schemas import Project, DataChunk
from typing import List
from stores.llm.LLMsEnum import DocumentTypeEnum
import json


class NLPController(BaseController):


    def __init__(self, vector_db_client, generation_client, embedding_client, template_parser):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project:Project):
        collection_name = self.create_collection_name(project.project_id)
        return self.vector_db_client.delete_collection(collection_name)
    
    def get_vector_db_collection_info(self, project:Project):
        collection_name = self.create_collection_name(project.project_id)
        collection_info = self.vector_db_client.get_collection_info(collection_name)

        return json.loads(
            json.dumps(collection_info, default= lambda o: o.__dict__))
    

    def index_into_vector_db(self, project:Project, chunks:List[DataChunk], chunks_ids:List[int], do_reset:bool=False):
        collection_name = self.create_collection_name(project.project_id)
        
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        vectors = [
            self.embedding_client.embed_text(text,DocumentTypeEnum.DOCUMENT.value)
             for text in texts 
        ]

        _= self.vector_db_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset,
        )

        _ = self.vector_db_client.insert_many(
            record_ids = chunks_ids,
            collection_name = collection_name,
            texts = texts,
            vectors = vectors,
            metadata = metadata
        )
        return True
    
    def search_vector_db_collection(self, project:Project, text:str, limit:int=5):
        collection_name = self.create_collection_name(project.project_id)
        
        vector = self.embedding_client.embed_text(text, DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False
        results = self.vector_db_client.search_by_vector(
            collection_name = collection_name,
            vector = vector,
            limit = limit
        )

        if not results:
            return False
        
        return results
     
        
    def answer_rag_question(self, project:Project, query:str, limit:int=5):
        answer, full_prompt, chat_history = None, None, None
        # retrieve related documents
        related_docs = self.search_vector_db_collection(project=project, text=query, limit=limit)
        
        if not related_docs or len(related_docs) == 0:
            return answer, full_prompt, chat_history
        
        # construct llm prompt
        system_prompt = self.template_parser.get("rag","system_prompt")

        documents_prompt = "\n".join([
            self.template_parser.get("rag","document_prompt",{
                "doc_num": idx+1,
                "chunk_text": doc.text
            })
            for idx,doc in enumerate(related_docs)
        ])

        footer_prompt = self.template_parser.get("rag","footer_prompt")

        chat_history = [
            self.generation_client.construct_prompt(
                prompt = system_prompt,
                role = self.generation_client.enums.SYSTEM.value,
            )
        ]
        full_prompt = "\n\n".join([documents_prompt,footer_prompt])


        answer = self.generation_client.generate_text(
            prompt = full_prompt,
            chat_history = chat_history,
        )

        return answer, full_prompt, chat_history