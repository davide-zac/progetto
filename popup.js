console.log("Popup script caricato.");

// Bottone per avviare la trasformazione
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    console.log("Bottone cliccato, avvio analisi...");

    try {
        // Ottieni la scheda attiva
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("Scheda attiva:", tab);

        // Esegui uno script per estrarre il testo da headings e paragrafi nella scheda attiva
        const extractedContent = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: extractPageContent, // Funzione eseguita nel contesto della pagina
        });

        // Controlla i risultati
        const { headings, paragraphs } = extractedContent[0].result;
        console.log("Contenuto estratto:", { headings, paragraphs });

        // Invia il testo al server Flask
        const response = await fetch('http://127.0.0.1:5000/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headings, paragraphs }),
        });

        const simplifiedData = await response.json();
        if (simplifiedData.error) {
            console.error("Errore dal server Flask:", simplifiedData.error);
            return;
        }

        console.log("Dati semplificati ricevuti dal server:", simplifiedData);

        // Sostituisci i contenuti nella pagina con quelli semplificati
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: injectSimplifiedContent,
            args: [simplifiedData], // Pass the simplified content to the content script
        });
    } catch (error) {
        console.error("Errore nell'analisi:", error);
    }
});

/**
 * Funzione per estrarre i contenuti di headings e paragrafi dalla pagina.
 * Viene eseguita nel contesto della pagina attiva.
 */
function extractPageContent() {
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.textContent.trim());
    const paragraphs = Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim());

    return { headings, paragraphs };
}

/**
 * Funzione per iniettare i contenuti semplificati nella pagina.
 * Viene eseguita nel contesto della pagina attiva.
 * @param {Object} simplifiedContent - Oggetto contenente headings e paragraphs semplificati.
 */
function injectSimplifiedContent(simplifiedContent) {
    console.log("Iniezione del contenuto semplificato nella pagina...");

    // Sostituisci titoli
    if (simplifiedContent.headings) {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
            if (simplifiedContent.headings[index]) {
                heading.textContent = simplifiedContent.headings[index];
            }
        });
    }

    // Sostituisci paragrafi
    if (simplifiedContent.paragraphs) {
        const paragraphs = document.querySelectorAll('p');
        paragraphs.forEach((paragraph, index) => {
            if (simplifiedContent.paragraphs[index]) {
                paragraph.textContent = simplifiedContent.paragraphs[index];
            }
        });
    }

    console.log("Contenuto semplificato iniettato con successo.");
}
