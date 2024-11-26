from typing import Optional, List, Mapping, Any
import requests, json
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings


class LMStudioLLM(CustomLLM):
    context_window: int = 3900
    num_output: int = 256
    model_name: str = "LMStudio"
    base_url: str = "http://localhost:1234/v1"  # URL del server LMStudio
    api_key: str = "lm-studio"  # Chiave API (se necessaria)

    def _send_request(self, prompt: str, stream: bool = False) -> requests.Response:
        """Invia una richiesta al server LMStudio."""
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "prompt": prompt,
            "max_tokens": self.num_output,
            "temperature": 0.5,
            "stream": stream,
        }
        response = requests.post(
            f"{self.base_url}/completions", json=payload, headers=headers, stream=stream
        )
        response.raise_for_status()
        return response

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Completamento sincrono."""
        try:
            response = self._send_request(prompt, stream=False)
            result = response.json()
            completion_text = result["choices"][0]["text"]
            return CompletionResponse(text=completion_text)
        except Exception as e:
            raise ValueError(f"Errore durante la richiesta al modello LMStudio: {e}")

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """Completamento asincrono (streaming) con gestione migliorata."""
        try:
            response = self._send_request(prompt, stream=True)
            response_text = ""
            print("Streaming iniziato...")
            for line in response.iter_lines(decode_unicode=True):
                if not line.strip():  # Ignora linee vuote
                    continue

                # Rimuovi il prefisso 'data: ' se presente
                if line.startswith("data: "):
                    line = line[len("data: "):]

                # Verifica se la linea è il segnale di fine streaming
                if line.strip() == "[DONE]":
                    print("Fine dello streaming.")
                    break

                try:
                    # Decodifica la linea come JSON
                    data = json.loads(line)
                    if "choices" in data and "text" in data["choices"][0]:
                        delta = data["choices"][0]["text"]

                        # Aggiungi solo il contenuto nuovo evitando ripetizioni
                        if not response_text.endswith(delta):
                            response_text += delta
                            # Stampa solo il delta per evitare confusione iniziale
                            print(delta, end="", flush=True)
                            yield CompletionResponse(text=response_text, delta=delta)
                except json.JSONDecodeError as e:
                    # Log per capire il problema
                    print(f"Errore nel parsing JSON: {e}, linea ricevuta: {line}")
        except requests.RequestException as e:
            raise ValueError(f"Errore nella comunicazione con il server LMStudio: {e}")
        except Exception as e:
            raise ValueError(f"Errore durante la richiesta in streaming: {e}")






