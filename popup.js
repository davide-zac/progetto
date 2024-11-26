console.log("Popup script caricato.");

// Bottone per avviare la trasformazione
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    console.log("Bottone cliccato, avvio analisi...");

    try {
        // Ottieni la scheda attiva
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("Scheda attiva:", tab);

        // Recupera l'URL della scheda attiva
        const pageUrl = tab.url;
        console.log("URL della pagina:", pageUrl);

        // Invia la richiesta al server Flask
        const response = await fetch('http://127.0.0.1:5000/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: pageUrl }),
        });

        const data = await response.json();
        if (data.error) {
            console.error("Errore dal server Flask:", data.error);
            return;
        }

        const transformedHtml = data.transformed_html;
        console.log("HTML trasformato ricevuto:", transformedHtml);

        // Aggiorna dinamicamente la pagina corrente
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: replacePageContent,
            args: [transformedHtml],
        });
    } catch (error) {
        console.error("Errore durante l'analisi della pagina:", error);
    }
});

// Funzione per sostituire il contenuto HTML della pagina
function replacePageContent(transformedHtml) {
    console.log("Sostituisco il contenuto della pagina con l'HTML trasformato.");
    document.documentElement.innerHTML = transformedHtml;
}



  
  