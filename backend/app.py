import re
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
from alternative_custom_chat import CustomLLM, custom_chat

app = Flask(__name__)
CORS(app)
llm = CustomLLM(
    model_name="meta-llama-3.1-8b-instruct",
    base_url="http://localhost:1234/v1",
    temperature=0.5,
)

# Funzione per trasformare i marcatori Markdown-like in HTML
def transform_markdown_to_html(text):
    # Rimpiazza i marcatori per il grassetto
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Rimpiazza i marcatori per il corsivo
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Aggiungi interruzioni di riga per i ritorni a capo espliciti
    text = text.replace('\n', '<br>')
    return text

def fetch_and_transform_with_llama(url):
    try:
        # Effettua la richiesta alla pagina
        response = requests.get(url)
        response.raise_for_status()  # Controlla se la richiesta è andata a buon fine

        # Analizza l'HTML della pagina
        soup = BeautifulSoup(response.content, "html.parser")

        # Identifica i tag rilevanti
        # ['title', 'h1', 'h2', 'h3', 'p', 'div']
        relevant_tags = ['title', 'p', 'div']
        min_text_length = 80  # Lunghezza minima per considerare un testo "rilevante"

        # Step 1: Raccogli i testi rilevanti
        elements_to_transform = []  # Lista di tuple (element, original_text)
        
        def collect_texts(element):
            # Salta nodi speciali come NavigableString o Doctype
            if isinstance(element, NavigableString) or element.name is None:
                return

            # Trasforma solo i tag rilevanti con testo abbastanza lungo
            if element.name in relevant_tags and element.string:
                text = element.string.strip()
                if len(text) >= min_text_length:
                    elements_to_transform.append((element, text))
            else:
                for child in element.children:  # Analizza ricorsivamente
                    collect_texts(child)

        collect_texts(soup)

        # Step 2: Esegui una singola query a Llama per trasformare i testi
        texts_to_transform = [text for _, text in elements_to_transform]
        transformed_texts = []

        try:
            transformed_texts = [custom_chat(llm, text) for text in texts_to_transform]
        except Exception as e:
            print(f"Errore durante la trasformazione con Llama: {e}")
            transformed_texts = texts_to_transform  # In caso di errore, usa i testi originali

        # Step 3: Applica le trasformazioni alla struttura originale
        for (element, original_text), transformed_text in zip(elements_to_transform, transformed_texts):
            # Applica la trasformazione Markdown-to-HTML al testo trasformato
            html_transformed = transform_markdown_to_html(transformed_text)
            # Sostituisci il testo trasformato nell'elemento
            element.string.replace_with(BeautifulSoup(html_transformed, "html.parser"))

        # Correggi i percorsi delle risorse per preservare il frontend
        for tag in soup.find_all(["link", "script", "img"]):
            if tag.has_attr("href"):  # Corregge i link CSS o altri file
                tag["href"] = urljoin(url, tag["href"])
            if tag.has_attr("src"):  # Corregge i link a script o immagini
                tag["src"] = urljoin(url, tag["src"])

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
    transformed_html = fetch_and_transform_with_llama(url)
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


