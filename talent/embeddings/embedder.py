import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from talent.embeddings.pinecone_client import index as PineconeIndex

from langchain_pinecone import PineconeVectorStore

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.environ["OPENAI_API_KEY"])

def generate_embeddings(chunks):
    return embeddings.embed_documents(chunks)


def store_embeddings_in_pinecone(chunks, embeddings):
    vectors = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append((str(i), embedding, {"text": chunk}))

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

def get_answer(query):
    llm = OpenAI(temperature=0.0)
    # Create Pinecone retriever instance
    vector_store = PineconeVectorStore(index=PineconeIndex, embedding=embeddings)
    system_prompt = """You are a highly intelligent system whose only job is to take in the query of a user, search through
    the data and return a JSON list of relevant candidates with respect to the query being made. If you are asked anything else,
    please respond with an empty list. If you do find relevant candidates, then use the following JSON format to return them:
    first_name, last_name, email, relevant_skills, match_percentage, experiences. If you do not find the email of the candidate,
    ignore that candidate.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', system_prompt),
            ('human', "{query}"),
            ('assistant', "Here are the relevant candidates I found for you: {context}"),
        ]
    )

    # Define retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    retrieved_docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs])


    answer = chain.invoke({"query": query, "context": context})

    return answer






