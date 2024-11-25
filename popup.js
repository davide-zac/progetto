console.log("Popup script caricato.");

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    console.log("Bottone cliccato, avvio analisi...");
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("Scheda attiva:", tab);

        // Invia l'URL della pagina al server Flask
        const response = await fetch('http://127.0.0.1:5000/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url }),
        });

        if (response.ok) {
            // Crea un blob e scarica il file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'transformed_page.html';
            document.body.appendChild(a);
            a.click();
            a.remove();
            console.log("File HTML trasformato scaricato.");
        } else {
            console.error("Errore nella trasformazione della pagina:", await response.text());
        }
    } catch (error) {
        console.error("Errore nell'analisi della pagina:", error);
    }
});


  
  