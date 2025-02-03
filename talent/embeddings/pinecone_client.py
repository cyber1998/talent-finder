import os

from pinecone import Pinecone

INDEX = 'resume-recommender'

pinecone_obj = Pinecone(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))

existing_indexes = pinecone_obj.list_indexes()

index = pinecone_obj.Index(INDEX, host="https://resume-recommender-te9leun.svc.aped-4627-b74a.pinecone.io")
