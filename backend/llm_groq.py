import re
import markdown
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
                        7. Use html elements to ensure an optimal reading experience
                Note: Rewrite using that language in the user text.
             """

text = """Vladimir Putin has threatened to strike Kyiv with Oreshnik missiles, an intermediate-range weapon that Moscow used against the city of Dnipro last week and that Putin has claimed cannot be shot down by any air defence system.
“We do not rule out the use of Oreshnik against the military, military-industrial facilities or decision-making centres, including in Kyiv,” Putin said at a press conference in Kazakhstan on Thursday. He said the weapon was “comparable in strength to a nuclear strike” if used several times on one location, though he added that it was not currently fitted with nuclear warheads.
“The kinetic impact is powerful, like a meteorite falling,” Putin said. “We know in history what meteorites have fallen where, and what the consequences were. Sometimes it was enough for whole lakes to form.”
The Ukrainian president, Volodymyr Zelenskyy, accused Russia of a “despicable escalation”.
Moscow has said the new threats are a response to a decision earlier this month by the US, Britain and France to allow Ukraine to fire long-range missiles provided by them against military targets inside Russia, something Kyiv had long requested.
Kyiv is better protected than most other Ukrainian cities by air defence batteries, and there have been few successful strikes on the centre of the capital during almost three years of war. Mykhailo Podolyak, an adviser to the Ukrainian president described Putin’s claim that air defence systems could not take out Oreshnik missiles as “fiction, of course”."""

chat_completion = client.chat.completions.create(
    messages =  [
        {"role": "system", "content": guidelines},
        # Set a user message for the assistant to respond to.
        {"role": "user", "content": text,}],
    model="llama3-8b-8192",
)

#print(chat_completion.choices[0].message.content)

# Funzione per trasformare i marcatori Markdown-like in HTML
def old_transform_markdown_to_html(text):
    # Rimpiazza i marcatori per il grassetto
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Rimpiazza i marcatori per il corsivo
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub('*','<li>')
    # Aggiungi interruzioni di riga per i ritorni a capo espliciti
    text = text.replace('\n', '<br>')
    return text


def transform_markdown_to_html(text):
    # Rimpiazza i marcatori per i list items
    text = re.sub(r'^\* (.+)', r'<li>\1</li>', text, flags=re.MULTILINE)
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
    
    # Prepare content to process
    simplified_headings = []
    for heading in headings:
        #print(heading)
        if len(heading)>100:
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
        if len(paragraph)>100 and j<1:
            chat_completion = client.chat.completions.create(
            messages =  [{"role": "system", "content": guidelines},
                        # Set a user message for the assistant to respond to.
                        {"role": "user", "content": paragraph,}],
            model="llama-3.1-70b-versatile",) #"llama-3.1-8b-instant",)     #"llama3-8b-8192",)
            simple_paragraph = chat_completion.choices[0].message.content

            # MARKDOWN TO HTML (if needed)
            simple_paragraph = transform_markdown_to_html(simple_paragraph)
            #print(simple_paragraph)
            #simple_paragraph = markdown.markdown(simple_paragraph)
            simplified_paragraphs.append(simple_paragraph)
        else:
            simplified_paragraphs.append(paragraph)
    
    # Return the results in the required format
    return {
        "headings": simplified_headings,
        "paragraphs": simplified_paragraphs
    }
