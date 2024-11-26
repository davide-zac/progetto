from customizing_llm import LMStudioLLM
from llama_index.core import PromptTemplate

llm=LMStudioLLM()
# Domanda diretta usando il metodo `complete`
question = "Qual è la capitale della Francia?"
# response = llm.complete(prompt=question)
# print(response.text)
# metodo stream_complete per generare la risposta in streaming
# question = "Qual è la capitale della Francia?"
# for token in llm.stream_complete(question):
#     print(token, end="", flush=True)


