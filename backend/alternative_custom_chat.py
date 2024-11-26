from llama_index.llms.lmstudio import LMStudio
from llama_index.core.prompts import ChatMessage, MessageRole
from typing import List
import httpx
import json
import logging

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

class CustomLLM(LMStudio):
    def chat(self, messages: List[ChatMessage], stream: bool = False, timeout: float = 300.0) -> str:
        # Aggiungi il tuo system prompt con regole precise in forma di prompt
        system_prompt = ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                "You are an expert AI assistant. Please follow these rules strictly while generating responses: "
                "1. Be concise and to the point. "
                "2. Always provide sources when giving factual information. "
                "3. Use a friendly and professional tone. "
                "4. Avoid any sensitive or controversial topics. "
                "5. Structure responses in short paragraphs."
            ),
        )
        messages.insert(0, system_prompt)
        messages_dict = [self.chat_message_to_dict(msg) for msg in messages]

        return self.send_request(messages_dict, stream, timeout)

    def chat_message_to_dict(self, chat_message):
        return {
            "role": chat_message.role.value,
            "content": chat_message.content
        }

    def send_request(self, messages_dict, stream: bool, timeout: float) -> str:
        full_response = ""
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                json={"messages": messages_dict, "options": {"temperature": 0.5, "stream": stream}},
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            full_response = ''.join(choice['message']['content'] for choice in data['choices'])
        except httpx.RequestError as e:
            logging.error(f"Errore durante la richiesta: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"Errore HTTP: {e}")
        except (ValueError, KeyError) as e:
            logging.error(f"Errore durante la decodifica o l'accesso ai dati: {e}")

        return full_response

# Inizializza la tua LLM personalizzata
llm = CustomLLM(
    model_name="meta-llama-3.1-8b-instruct",
    base_url="http://localhost:1234/v1",
    temperature=0.5,
)

# Definisci i tuoi messaggi utente
messages = [
    ChatMessage(
        role=MessageRole.USER,
        content="What is the significance of the number 42?",
    ),
]

# Usa la tua LLM personalizzata con timeout personalizzato
response = llm.chat(messages=messages, timeout=600.0)  # Timeout di 600 secondi
print(response)

