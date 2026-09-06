from ingestion.document_loader import load_documents
from ingestion.document_chunker import chunk_documents
from vectorstore.chroma_store import create_vectorstore


documents = load_documents()

chunks = chunk_documents(documents)

create_vectorstore(chunks)

print("Vector store created successfully!")