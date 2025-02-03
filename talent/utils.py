import PyPDF2
from langchain.text_splitter import CharacterTextSplitter

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    return text


def split_text(text, max_chars=1024):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=max_chars,
        chunk_overlap=max_chars//16,
        length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks
