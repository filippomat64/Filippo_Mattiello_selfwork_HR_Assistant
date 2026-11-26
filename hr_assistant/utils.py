
from .config import Config
from openai import OpenAI

client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)


class LLMHelper:

    @staticmethod
    def chat(messages):
        return client.chat.completions.create(
            model=Config.LLM_MODEL, messages=messages, stream=True
        )

    @staticmethod
    def create_prompt(context, question):
        return f"""
            Dato il seguente contesto:

            [[[
            {context}
            ]]]

            Rispondi alla domanda dell'utente:
            [[[ {question} ]]]

            Individua il candidato più adatto alla richiesta.

            Nella risposta indica:
            - Nome e cognome del candidato.
            - Indirizzo email, se presente.
            - Numero di telefono, se presente.
            - Nome del file del curriculum.

            Argomenta la scelta utilizzando le informazioni
            presenti nel curriculum.

            Se non trovi corrispondenza in nessun CV,
            non inventare informazioni.

            Non inventare dati personali mancanti.
        """
