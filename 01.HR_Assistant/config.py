import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "text-embedding-3-small"
    PERSISTENT_DIR = "chroma_db"
    COLLECTION_NAME = "hr_documents"
    DOCUMENTS_DIR = "documents"