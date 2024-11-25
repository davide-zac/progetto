console.log("Popup script caricato.");

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    console.log("Bottone cliccato, avvio analisi...");
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("Scheda attiva:", tab);

        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: extractTextContent,
        }, async (results) => {
          console.log("Risultati dello script:", results);

          if (results && results[0] && results[0].result) {
            const pageContent = results[0].result;
            console.log("Contenuto della pagina:", pageContent);

            const response = await fetch('http://127.0.0.1:5000/count', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ text: pageContent }),
            });

            const data = await response.json();
            console.log("Risposta dal server Flask:", data);

            document.getElementById('result').textContent = `Occorrenze di "Juventus": ${data.count}`;
          } else {
            console.error("Errore: Nessun risultato dallo script.");
          }
        });
    } catch (error) {
        console.error("Errore nell'analisi della pagina:", error);
    }
});

function extractTextContent() {
    console.log("Eseguo extractTextContent sulla pagina.");
    return document.body.innerText;
}

  
  