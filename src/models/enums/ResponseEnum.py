from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCCESS = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOADED_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    FILE_PROECSSING_SUCCESS = "file_processing_successfully"
    FILE_PROECSSING_FAILED = "file_processing_failed"
    FILE_NOT_FOUND = "file_not_found"
    NO_FILE_WITH_ID = "no_file_with_id_found"
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSER_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSER_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTOR_COLLECTION_RETRIEVED = "vector_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"