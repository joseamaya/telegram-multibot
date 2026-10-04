from langgraph.store.mongodb import create_vector_index_config

from ai.embeddings import get_embeddings

EMBEDDING_DIMENSION = 1536


def get_index_config():
    """Configuración del índice vectorial para la búsqueda semántica del store."""
    return create_vector_index_config(
        embed=get_embeddings(),
        dims=EMBEDDING_DIMENSION,
    )
