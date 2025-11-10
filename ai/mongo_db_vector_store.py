from typing import Optional, Dict, ClassVar
from functools import lru_cache
from langchain_mongodb import MongoDBAtlasVectorSearch

from ai.embeddings import get_embeddings
from database.connection import MongoDBConnection


class MongoDBVectorStore:
    _instances: ClassVar[Dict[str, MongoDBAtlasVectorSearch]] = {}
    EMBEDDING_DIMENSION = 1536

    @classmethod
    def get_instance(
        cls,
        collection_name: str,
        index_name: str,
        filters: Optional[list] = None
    ) -> MongoDBAtlasVectorSearch:
        instance_key = f"{collection_name}:{index_name}"
        if instance_key not in cls._instances:
            collection = cls._get_collection(collection_name)
            vector_store = cls._create_vector_store(collection, index_name)
            cls._ensure_vector_index(vector_store, collection, index_name, filters)
            cls._instances[instance_key] = vector_store
        return cls._instances[instance_key]

    @staticmethod
    def _get_collection(collection_name: str):
        MongoDBConnection.connect_to_sync_mongo()
        db = MongoDBConnection.get_sync_db()
        return db[collection_name]

    @staticmethod
    def _create_vector_store(collection, index_name: str) -> MongoDBAtlasVectorSearch:
        return MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=get_embeddings(),
            index_name=index_name,
            relevance_score_fn="cosine"
        )

    @classmethod
    def _ensure_vector_index(
        cls,
        vector_store: MongoDBAtlasVectorSearch,
        collection,
        index_name: str,
        filters: Optional[list]
    ):
        existing_indexes = collection.list_search_indexes()
        existing_names = [idx["name"] for idx in existing_indexes]
        if index_name not in existing_names:
            try:
                vector_store.create_vector_search_index(
                    dimensions=cls.EMBEDDING_DIMENSION,
                    filters=filters or []
                )
            except Exception as e:
                print(f"Warning: No se pudo crear el índice vectorial: {e}")


@lru_cache
def get_mongo_db_vector_store() -> MongoDBVectorStore:
    return MongoDBVectorStore()
