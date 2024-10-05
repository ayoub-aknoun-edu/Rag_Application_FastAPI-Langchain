from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"

class DistanceVectorEnums(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"