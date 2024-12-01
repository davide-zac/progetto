import re

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
    text = re.sub(r'\*(.+?)\*', r'<strong>\1</strong>', text)
    # Aggiungi interruzioni di riga per i ritorni a capo espliciti
    text = text.replace('\n', '<br>')
    text = text.replace('<br><br>','<br>')
    return text

def refine_html(text):
    # MARKDOWN TO HTML
    # Rimpiazza i marcatori per i list items
    text = re.sub(r'^\* (.+)', r'<li>\1</li>', text, flags=re.MULTILINE)
    # Rimpiazza i marcatori per il grassetto
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Rimpiazza i marcatori per il corsivo
    text = re.sub(r'\*(.+?)\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\<em>(.+?)\</em>', r'<strong>\1</strong>', text)
    
    #HTML TO HTML
    # Aggiungi interruzioni di riga per i ritorni a capo espliciti
    text = text.replace('\n', '<br>')
    # Paragrafi
    text = re.sub(r'\<p>(.+?)\</p>', r'<br>\1', text)
    # Elimina doppie interruzioni
    text = text.replace('<br><br>','')
    

    # Rimpiazza tutte le intestazioni fornite da llama con la più piccola intestazione
    text = re.sub(r'<h[1-6]>(.*?)</h[1-6]>', r'<br><h4>\1</h4>', text)
    return text