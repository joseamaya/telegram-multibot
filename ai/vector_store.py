import logging
import os

from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client

from ai.embeddings import get_embeddings

logger = logging.getLogger(__name__)

def create_supabase_vector_store():
    vector_store = None
    embeddings = get_embeddings()
    try:
        supabase = create_client(
            supabase_url=os.environ.get('SUPABASE_URL'),
            supabase_key=os.environ.get('SUPABASE_SERVICE_KEY')
        )
        vector_store = SupabaseVectorStore(
            client=supabase,
            embedding=embeddings,
            table_name="documents",
            query_name="match_documents"
        )
    except Exception as e:
        logger.error(f"Error creando vector store: {str(e)}")

    return vector_store