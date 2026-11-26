
import os
import uuid
from .config import Config


# Scegliamo quale tecnica di chunking utilizzare
CHUNKING_METHOD = "headings"


class DocumentProcessor:

    @staticmethod
    def process_documents():
        documents = []
        metadatas = []
        ids = []

        for filename in os.listdir(Config.DOCUMENTS_DIR):
            if filename.endswith(".txt"):
                with open(
                    os.path.join(Config.DOCUMENTS_DIR, filename),
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

                    # Tecnica 1: divisione tramite titoli
                    if CHUNKING_METHOD == "headings":
                        chunks = text.split("### ")

                    # Tecnica 2: divisione tramite paragrafi
                    elif CHUNKING_METHOD == "paragraphs":
                        chunks = text.split("\n\n")

                    # Tecnica 3: divisione ogni 500 caratteri
                    elif CHUNKING_METHOD == "fixed":
                        chunks = [
                            text[i:i + 500]
                            for i in range(0, len(text), 500)
                        ]

                    else:
                        chunks = [text]

                    for chunk in chunks:
                        if chunk.strip():
                            documents.append(chunk.strip())
                            metadatas.append({"source": filename})
                            ids.append(str(uuid.uuid4()))

        return documents, metadatas, ids

    @staticmethod
    def read_first_lines(file_path, n_lines=100):
        with open(file_path, "r", encoding="utf-8") as file:
            return [
                line.strip()
                for line, _ in zip(file, range(n_lines))
            ]
