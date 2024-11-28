from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import markdown
from IPython.display import display, Markdown, HTML

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
3. Simplified language: Use of simple terms and active sentences.
4. Elimination of unnecessary acronyms and symbols."""

    # Template for the LLM
    template = """You are a psychiatrist tackling dyslexia. Rewrite
this content to make it dyslexia friendly, following these guidelines: {guidelines}.
Content: {content}."""
    
    # Initialize the LLM model
    model = OllamaLLM(model="llama3.2")  # Update with the actual model initialization
    
    # Prepare content to process
    simplified_headings = []
    for heading in headings:
        print(heading)
        if len(heading)>100:
            '''# Format prompt for each heading
            prompt = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt.format(content=heading, guidelines=guidelines)
            # Get the response for the heading
            response = model.invoke(formatted_prompt)
            simplified_headings.append(response.strip())'''
            simplified_headings.append("Sto gran cazzo semplificato oeeeeeeh:" + heading)
        else:
            simplified_headings.append("Sto gran cazzo semplificato oeeeeeeh:" + heading)

    simplified_paragraphs = []
    for paragraph in paragraphs:
        print(paragraph)
        if len(paragraph)>500:
            '''# Format prompt for each paragraph
            prompt = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt.format(content=paragraph, guidelines=guidelines)
            # Get the response for the paragraph
            response = model.invoke(formatted_prompt)
            simplified_paragraphs.append(response.strip())'''
            simplified_paragraphs.append("Sto gran cazzo semplificato oeeeeeeh:" + paragraph)
        else:
            #simplified_paragraphs.append(paragraph)
            simplified_paragraphs.append("Sto gran cazzo semplificato oeeeeeeh:" + paragraph)
    
    # Return the results in the required format
    return {
        "headings": simplified_headings,
        "paragraphs": simplified_paragraphs
    }
