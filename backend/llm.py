from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import markdown
from IPython.display import display, Markdown, HTML

# Funzione per trasformare i marcatori Markdown-like in HTML
def transform_markdown_to_html(text):
    # Rimpiazza i marcatori per il grassetto
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Rimpiazza i marcatori per il corsivo
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Aggiungi interruzioni di riga per i ritorni a capo espliciti
    text = text.replace('\n', '<br>')
    return text

def simplify_content(headings, paragraphs):
    """
    Simplify the given headings and paragraphs using an LLM.
    
    Args:
        headings (list of str): List of headings from the page.
        paragraphs (list of str): List of paragraphs from the page.

    Returns:
        dict: A dictionary containing simplified headings and paragraphs.
    """
    # Guidelines for dyslexia-friendly content
    guidelines = """1. Short sentences: Each sentence expresses a single idea to reduce cognitive load.
                    2. Frequent headings: They help break the text into readable blocks.
                    3. Simplified language: Use simple terms and active sentences.
                    4. Elimination of unnecessary acronyms and symbols."""

    # Template for the LLM
    template = """Rewrite text content to make it dyslexia friendly, following these guidelines: {guidelines}.
                  Rewrite the following tedt: {content}.
                  DO NOT INSERT ANY NOTES OR COMMENTS, JUST OUTPUT THE TRANSFORMED TEXT"""
    
    # Initialize the LLM model
    model = OllamaLLM(model="llama3.2")  # Update with the actual model initialization
    
    # Prepare content to process
    simplified_headings = []
    for heading in headings:
        #print(heading)
        if len(heading)>100:
            '''
            # # Format prompt for each heading
            prompt = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt.format(content=heading, guidelines=guidelines)
            # Get the response for the heading
            response = model.invoke(formatted_prompt, max_tokens= len(heading))
            simplified_headings.append(response.strip())
            '''
            simplified_headings.append("Semplificato per finta" + heading)
        else:
            simplified_headings.append(heading)
            #simplified_headings.append("Sto gran cazzo semplificato oeeeeeeh:" + heading)

    simplified_paragraphs = []
    j = 0
    for paragraph in paragraphs:
        #print(paragraph)
        if len(paragraph)>100 and j<1:
            #'''
            # Format prompt for each paragraph
            print(paragraph)
            prompt = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt.format(content=paragraph, guidelines=guidelines)
            # Get the response for the paragraph
            response = model.invoke(formatted_prompt, max_tokens = len(paragraph))
            response = transform_markdown_to_html(response.strip())
            simplified_paragraphs.append(response)
            print(response)
            #j += 1
            #'''
            #simplified_paragraphs.append("Sto gran cazzo <strong>semplificato</strong> oeeeeeeh<br>" + paragraph)
        else:
            #simplified_paragraphs.append(paragraph)
            simplified_paragraphs.append("Semplificato per finta" + paragraph)
    
    # Return the results in the required format
    return {
        "headings": simplified_headings,
        "paragraphs": simplified_paragraphs
    }
