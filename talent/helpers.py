import io

from talent.embeddings.embedder import generate_embeddings, store_embeddings_in_pinecone, \
    get_answer
from talent.utils import extract_text_from_pdf, split_text


def process_resume(resume_file):
    """
    Extract text from a resume file
    """
    try:
        # Convert inmemory file to path like object
        text = extract_text_from_pdf(resume_file)
        chunks = split_text(text)
        embeddings = generate_embeddings(chunks)
        store_embeddings_in_pinecone(chunks, embeddings)
    except Exception as e:
        return False
    return True


def get_resumes(query, top_k=1):
    """
    Get resumes from Pinecone
    """
    try:
        answers = get_answer(query)
        return answers
    except Exception as e:
        return None
