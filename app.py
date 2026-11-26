
import os
import chainlit as cl

from hr_assistant.document_processor import DocumentProcessor
from hr_assistant.database import Database
from hr_assistant.config import Config
from hr_assistant.utils import LLMHelper


# Process documents
documents, metadatas, ids = DocumentProcessor.process_documents()

# Initialize database and add documents
db = Database()
db.add_documents(documents, metadatas, ids)


@cl.on_chat_start
def start():
    cl.user_session.set(
        "messages",
        [
            {
                "role": "system",
                "content": """
                    Sei un assistente specializzato nel mondo HR,
                    rispondi in modo professionale, sintetico e pragmatico.
                    Il tuo ruolo è individuare il candidato ideale
                    rispetto alle richieste dell'utente.
                """,
            }
        ],
    )


@cl.on_message
async def handle_message(message: cl.Message):

    try:
        print("DEBUG 1: domanda ricevuta", flush=True)

        user_question = message.content
        results = db.query(user_question)

        print("DEBUG 2: ricerca ChromaDB completata", flush=True)

        filename = results["metadatas"][0][0]["source"]

        context_lines = DocumentProcessor.read_first_lines(
            os.path.join(Config.DOCUMENTS_DIR, filename), 10
        )

        print("DEBUG 3: curriculum letto", flush=True)

        context = (
            f"INFORMAZIONI INIZIALI DEL CURRICULUM:\n"
            f"{chr(10).join(context_lines)}\n\n"
            f"CONTENUTO PIU' SIGNIFICATIVO:\n"
            f"{results['documents'][0][0]}\n\n"
            f"NOME FILE: {filename}"
        )

        prompt = LLMHelper.create_prompt(context, user_question)

        messages = cl.user_session.get("messages", [])
        messages.append({"role": "user", "content": prompt})

        response_message = cl.Message(content="")
        await response_message.send()

        print("DEBUG 4: avvio chiamata LLM", flush=True)

        stream = LLMHelper.chat(messages)

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                await response_message.stream_token(content)

        print("DEBUG 5: streaming terminato", flush=True)

        messages.append(
            {"role": "assistant", "content": response_message.content}
        )

        await response_message.update()

        cl.user_session.set("messages", messages)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()
        print("ERRORE:", error_message, flush=True)
