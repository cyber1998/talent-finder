from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from talent.embeddings.pinecone_client import index as PineconeIndex

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

load_dotenv('.env')

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def generate_embeddings(chunks):
    return embeddings.embed_documents(chunks)


def store_embeddings_in_pinecone(chunks, embeddings):
    vectors = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append((str(i), embedding, {"text": chunk}))

    PineconeIndex.upsert(vectors)

def get_embeddings_from_pinecone(query, top_k=5):
    query_embedding = embeddings.embed_query(query)
    results = PineconeIndex.query(query_embedding, top_k=top_k, include_metadata=True)
    return results


def get_answer(query, results):
    llm = OpenAI(temperature=0.0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=results)
    answer = qa.run(query)
    return answer






