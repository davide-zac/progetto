from flask import Flask, request, jsonify, send_file
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
@app.route('/transform', methods=['POST'])
def transform_html():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Nessun URL fornito'}), 400

    # Trasforma il contenuto della pagina
    transformed_html = fetch_and_transform_page(url)
    if not transformed_html:
        return jsonify({'error': 'Impossibile recuperare o trasformare la pagina'}), 500

    # Salva il file trasformato
    output_path = 'transformed_page.html'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(transformed_html)

    # Restituisce il file come risposta
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

