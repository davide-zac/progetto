import markdown
from utils import *
from groq import Groq

client = Groq(
    api_key="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",
)


guidelines = """Rewrite text content to make it dyslexia friendly, following these guidelines:
                        1. Short sentences: Each sentence expresses a single idea to reduce cognitive load.
                        2. Frequent headings: They help break the text into readable blocks.
                        3. Simplified language: Use simple terms and active sentences.
                        4. Elimination of unnecessary acronyms and symbols.
                        5. DO NOT INSERT ANY NOTES OR COMMENTS, JUST OUTPUT THE TRANSFORMED TEXT
                        6. For each paragraph add a heading
                Note: Rewrite using that language in the user text.
             """
# 7. Use html elements to ensure an optimal reading experience


#print(chat_completion.choices[0].message.content)

# Funzione per trasformare i marcatori Markdown-like in HTML



def simplify_content(headings, paragraphs):
    """
    Simplify the given headings and paragraphs using an LLM.
    
    Args:
        headings (list of str): List of headings from the page.
        paragraphs (list of str): List of paragraphs from the page.

    Returns:
        dict: A dictionary containing simplified headings and paragraphs.
    """
    
    # Prepare content to process
    simplified_headings = []
    for heading in headings:
        #print(heading)
        if len(heading)>69:
            #'''
            chat_completion = client.chat.completions.create(
            messages =  [{"role": "system", "content": guidelines},
                        # Set a user message for the assistant to respond to.
                        {"role": "user", "content": heading,}],
            model= "llama-3.1-70b-versatile",) #"llama-3.1-8b-instant",)     #"llama3-8b-8192",)
            simple_heading = chat_completion.choices[0].message.content
            
            # MARKDOWN TO HTML (if needed)
            simple_heading = transform_markdown_to_html(simple_heading)
            #simple_heading = markdown.markdown(simple_heading)

            simplified_headings.append(simple_heading)
        else:
            simplified_headings.append(heading)


    simplified_paragraphs = []
    j = 0
    for paragraph in paragraphs:
        #print(paragraph)
        if len(paragraph)>100 and j<10:
            chat_completion = client.chat.completions.create(
            messages =  [{"role": "system", "content": guidelines},
                        # Set a user message for the assistant to respond to.
                        {"role": "user", "content": paragraph,}],
            model="llama-3.1-70b-versatile",) #"llama-3.1-8b-instant",)     #"llama3-8b-8192",)
            simple_paragraph = chat_completion.choices[0].message.content

            # MARKDOWN TO HTML (if needed)
            simple_paragraph = transform_markdown_to_html(simple_paragraph) #refine_html(simple_paragraph)
            print(simple_paragraph)
            #simple_paragraph = markdown.markdown(simple_paragraph)
            simplified_paragraphs.append(simple_paragraph)
            j += 1
        else:
            simplified_paragraphs.append(paragraph)
    
    # Return the results in the required format
    return {
        "headings": simplified_headings,
        "paragraphs": simplified_paragraphs
    }
