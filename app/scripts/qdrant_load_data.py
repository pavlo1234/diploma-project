from qdrant_client import models, QdrantClient
from pymongo import MongoClient
from google import genai
from google.genai import types


GOOGLE_API_KEY = "**************************************"
MONGODB_URL = "mongodb://localhost:27017/"
QDRANT_URL = "http://localhost:6333"

db_client = MongoClient(MONGODB_URL)

activities = db_client.project.activities

ai_client = genai.Client(api_key=GOOGLE_API_KEY)

embedding_model = "models/embedding-001"  

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


q_client = QdrantClient(url="http://localhost:6333")

if not q_client.collection_exists("activities"):
    q_client.recreate_collection(
        collection_name="activities",
        vectors_config=models.VectorParams(
            size=768,  # Vector size is defined by used model
            distance=models.Distance.COSINE,
        ),
    )

try:
    points = []
    for activity in activities.find():
        activity["_id"] = str(activity["_id"])
        response = ai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Summarize this data into text: {str(activity)}"],
            config=types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=1
            )
        )
        points += [models.PointStruct(id=activity["id"], vector=make_embed_text_fn(response.text), payload = activity)]

    q_client.upsert(
        collection_name="activities",
        points=points
    )
    print("Data has been loaded successfully.")
except Exception as e:
    print(f"Error occured: {e}")
