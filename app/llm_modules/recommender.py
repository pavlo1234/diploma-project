
import os 

from google import genai
from google.genai import types

from qdrant_client import QdrantClient

from ..models.activities import Activity

ai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
embedding_model = "models/embedding-001"

q_client = QdrantClient(os.environ["QDRANT_URL"])


def make_embed_text_fn(text, model=embedding_model,
                       task_type="retrieval_document"):
    embedding = ai_client.models.embed_content(
        model=model,
        contents=text,
        config=types.EmbedContentConfig(
          task_type=task_type,
        )
    )
    return embedding.embeddings[0].values

prompt = '''
    You need to make recommendations for users, that want to find activities they can like.
    Your task is to retrieve possible keywords, that can describe activities, that given user likes
    This is user query: {query}
    Give comma-separated keywords:
    '''

def get_recommendations(query: str) -> list[Activity]:

    query_enhanced = ai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt.format(query=query)],
    )
    
    hits = q_client.search(
        collection_name="activities",
        query_vector=make_embed_text_fn(query_enhanced.text, task_type="retrieval_query"),
        limit=3,
    )

    prompt_gen = f'''
    These are activities, that user may like: 
    {';'.join(str(hit.payload) for hit in hits)}.
    User query is: {query}.
    Keywords: {query_enhanced.text}.
    List these activities.
    '''

    result = ai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt_gen],
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Activity],
        }
    )

    return result.parsed