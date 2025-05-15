from ai.vector_store import create_supabase_vector_store


def get_retriever(k=3):
    vector_store = create_supabase_vector_store()
    if vector_store:
        return vector_store.as_retriever(search_kwargs={"k": k})
    return None