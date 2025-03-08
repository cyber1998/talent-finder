import os
import uuid

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from talent.embeddings.pinecone_client import index as PineconeIndex

from langchain_pinecone import PineconeVectorStore

from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.environ["OPENAI_API_KEY"])

def generate_embeddings(chunks):
    return embeddings.embed_documents(chunks)


def store_embeddings_in_pinecone(chunks, embeddings):
    vectors = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append((str(uuid.uuid4()), embedding, {"text": chunk}))

    PineconeIndex.upsert(vectors)

def pinecone_to_documents(results):
    documents = []
    for match in results.matches:
        text = match.metadata.get("text", "")
        documents.append(Document(page_content=text))
    return documents

def pinecone_retriever(query, index, embeddings, top_k=5):
    query_embedding = embeddings.embed_query(query)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return pinecone_to_documents(results)

def get_answer(input):
    llm = OpenAI(temperature=0.0, max_tokens=2048)
    # Create Pinecone retriever instance
    vector_store = PineconeVectorStore(index=PineconeIndex, embedding=embeddings)
    system_prompt = """You are a highly intelligent AI bot named Stanley who is an expert in hiring senior software engineers.
    {context}
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', system_prompt),
            ('human', """"{input}. Structure the response as a list of JSON objects with the following keys:
            
            first_name: str,
            last_name: str,
            email: str,
            relevant_skills: List[str],
            experiences: List[str], # Summarized experiences of the candidate
            match_percentage: str]
            
            If no email is found for the candidate, ignore that candidate. Limit the results to 10 candidates.
            """),
        ]
    )

    # Define retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    # retrieved_docs = retriever.get_relevant_documents(query)
    # context = "\n".join([doc.page_content for doc in retrieved_docs])


    answer = chain.invoke({"input": input})

    return answer






