from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def fetch_and_parse_page(url):
    """
    Recupera il contenuto di una pagina web e organizza il testo in base ai tag HTML principali.

    Args:
        url (str): URL della pagina web da analizzare.

    Returns:
        dict: Dizionario con i tag HTML come chiavi e una lista di testi associati a ciascun tag.
    """
    try:
        # Richiesta HTTP per ottenere il contenuto della pagina
        response = requests.get(url)
        response.raise_for_status()  # Verifica che non ci siano errori HTTP
        html_content = response.text

        # Parsing del contenuto HTML con BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Dizionario per organizzare i testi per tag
        text_by_tag = {}

        # Lista di tag da analizzare (aggiungi altri se necessario)
        tags_to_extract = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote']

        for tag in tags_to_extract:
            # Trova tutti gli elementi di un determinato tag
            elements = soup.find_all(tag)

            # Estrai il testo da ciascun elemento e rimuovi spazi extra
            text_list = [element.get_text(strip=True) for element in elements]

            # Aggiungi al dizionario solo se ci sono testi per quel tag
            if text_list:
                text_by_tag[tag] = text_list

        return text_by_tag

    except requests.exceptions.RequestException as e:
        print(f"Errore durante il recupero della pagina: {e}")
        return {"error": "Impossibile recuperare la pagina web"}
def fetch_and_transform_page(url):
    try:
        # Effettua la richiesta alla pagina
        response = requests.get(url)
        response.raise_for_status()  # Controlla se la richiesta è andata a buon fine
        
        # Analizza l'HTML della pagina
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Funzione ricorsiva per trasformare il testo in maiuscolo e preservare la struttura
        def transform_text(element):
            if element.string:  # Se è un nodo di testo
                element.string = element.string.upper()  # Trasforma il testo in maiuscolo
            else:
                for child in element.children:  # Se ha figli, ricorri
                    transform_text(child)

        # Applica la trasformazione alla struttura principale
        transform_text(soup)

        # Restituisce l'HTML modificato
        return str(soup)

    except requests.exceptions.RequestException as e:
        print(f"Errore durante il recupero della pagina: {e}")
        return None
'''
# Esempio di utilizzo
if __name__ == "__main__":
    url = "https://example.com"  # Sostituisci con l'URL desiderato
    transformed_html = fetch_and_transform_page(url)
    
    if transformed_html:
        print("Struttura HTML trasformata:\n")
        print(transformed_html)  # Stampa l'HTML modificato
'''
@app.route('/count', methods=['POST'])
def count_occurrences():
    """
    Endpoint per contare le occorrenze della parola "Juventus" o per analizzare un URL.

    Returns:
        JSON: Conteggio delle occorrenze o struttura di testo analizzata.
    """
    data = request.get_json()
    text = data.get('text', '')
    url = data.get('url', None)

    if url:
        # Analizza il contenuto di una pagina web se viene passato un URL
        parsed_text = fetch_and_transform_page(url)
        return jsonify(parsed_text)
    elif text:
        # Conta le occorrenze della parola "Juventus" nel testo
        count = text.lower().count("juventus")
        return jsonify({'count': count})
    else:
        return jsonify({"error": "Nessun testo o URL fornito"}), 400


if __name__ == '__main__':
    app.run(debug=True)


