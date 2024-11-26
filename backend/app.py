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


    
def fetch_and_transform_page_phase0(url):
    try:
        # Effettua la richiesta alla pagina
        response = requests.get(url)
        response.raise_for_status()  # Controlla se la richiesta è andata a buon fine
        
        # Analizza l'HTML della pagina
        soup = BeautifulSoup(response.content, "html.parser")

        # Funzione ricorsiva per trasformare il testo in maiuscolo
        def transform_text(element):
            for child in element.children:
                if isinstance(child, NavigableString):  # Se è un nodo di testo
                    child.replace_with(child.upper())  # Trasforma il testo in maiuscolo
                elif child.name:  # Se è un tag, ricorri
                    transform_text(child)

        # Trasforma il testo principale della pagina
        transform_text(soup)

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




def fetch_and_transform_with_llama(url):
    try:
        # Effettua la richiesta alla pagina
        response = requests.get(url)
        response.raise_for_status()  # Controlla se la richiesta è andata a buon fine
        
        # Analizza l'HTML della pagina
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Identifica i tag rilevanti
        # ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote']  
        relevant_tags = ['title', 'h1', 'h2', 'h3', 'p', 'div']
        min_text_length = 50  # Lunghezza minima per considerare un testo "rilevante"

        # Funzione ricorsiva per trasformare i testi
        def transform_text(element):
            # Salta i nodi di tipo NavigableString e Doctype 
            if isinstance(element, NavigableString) or element.name is None: 
                return
            
            if element.name in relevant_tags and element.string:
                # Controlla se il testo è sufficientemente lungo
                text = element.string.strip()
                if len(text) >= min_text_length:
                    print(f"Testo rilevante trovato: {text}")
                    # Usa LlamaIndex per ottenere la trasformazione
                    transformed_text = custom_chat(llm,text)
                    element.string = transformed_text  # Sostituisci il testo
            else:
                for child in element.children:# Se ha figli, ricorri
                        transform_text(child)

                    

        # Applica la trasformazione alla struttura principale
        transform_text(soup)

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

