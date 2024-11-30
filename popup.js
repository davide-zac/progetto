console.log("Popup script caricato.");

// Bottone per avviare la trasformazione
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    console.log("Bottone cliccato, avvio analisi...");

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log("Scheda attiva:", tab);

        const extractedContent = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: extractPageContent,
        });

        const { headings, paragraphs } = extractedContent[0].result;
        console.log("Contenuto estratto:", { headings, paragraphs });

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

        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: injectSimplifiedContent,
            args: [simplifiedData],
        });
    } catch (error) {
        console.error("Errore nell'analisi:", error);
    }
});

// Dropdown per cambiare il font
document.getElementById('fontSelect').addEventListener('change', async (event) => {
    const selectedFont = event.target.value;
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Execute the changeFont function in the context of the active tab
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: changeFont,
        args: [selectedFont] // Pass the selected font as an argument
    });
});

function extractPageContent() {
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.textContent.trim());
    const paragraphs = Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim());
    return { headings, paragraphs };
}

function injectSimplifiedContent(simplifiedContent) {
    if (simplifiedContent.headings) {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
            if (simplifiedContent.headings[index]) {
                heading.innerHTML = simplifiedContent.headings[index];
            }
        });
    }

    if (simplifiedContent.paragraphs) {
        const paragraphs = document.querySelectorAll('p');
        paragraphs.forEach((paragraph, index) => {
            if (simplifiedContent.paragraphs[index]) {
                paragraph.innerHTML = simplifiedContent.paragraphs[index];
            }
        });
    }
}

function changeFont(font) {
    if (font === 'OpenDyslexic') {
        // Inject the font if not already present
        const styleId = 'open-dyslexic-font';
        let styleElement = document.getElementById(styleId);

        if (!styleElement) {
            styleElement = document.createElement('style');
            styleElement.id = styleId;
            styleElement.innerHTML = `
                @font-face {
                    font-family: 'OpenDyslexic';
                    src: url(${chrome.runtime.getURL('fonts/OpenDyslexic-Regular.otf')}) format('opentype');
                }
            `;
            document.head.appendChild(styleElement);
        }

        // Apply the OpenDyslexic font to the body
        document.body.style.fontFamily = 'OpenDyslexic, sans-serif';
    } else {
        // Apply other fonts
        document.body.style.fontFamily = font;
    }
}

