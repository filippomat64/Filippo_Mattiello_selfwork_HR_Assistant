import chainlit as cl
from document_processor import DocumentProcessor
from database import Database

# Process documents
documents, metadatas, ids = DocumentProcessor.process_documents()

# Initialize database and add documents
db = Database()
db.add_documents(documents, metadatas, ids)


@cl.on_message
async def handle_message(message: cl.Message):
    user_question = message.content

    results = db.query(user_question)

    response = results["documents"][0][0]

    await cl.Message(content=response).send()