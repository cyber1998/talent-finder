import pinecone
from dotenv import load_dotenv
import os

load_dotenv('.env')
INDEX = 'resume-recommender'

pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment='us-east-1')

if INDEX not in pinecone.list_indexes():
    pinecone.create_index(name=INDEX, metric='cosine', shards=1, dimension=1536)

index = pinecone.Index(INDEX, host="https://resume-recommender-te9leun.svc.aped-4627-b74a.pinecone.io")



