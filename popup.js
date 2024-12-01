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

        await processBatches(headings, paragraphs, tab);
    } catch (error) {
        console.error("Errore nell'analisi:", error);
    }
});

async function processBatches(headings, paragraphs, tab) {
    const batchSize = 3;
    let headingOffset = 0; // Tracks where to inject headings
    let paragraphOffset = 0; // Tracks where to inject paragraphs

    const totalBatches = Math.ceil(Math.max(headings.length, paragraphs.length) / batchSize);

    for (let batchIndex = 0; batchIndex < totalBatches; batchIndex++) {
        const headingBatch = headings.slice(batchIndex * batchSize, (batchIndex + 1) * batchSize);
        const paragraphBatch = paragraphs.slice(batchIndex * batchSize, (batchIndex + 1) * batchSize);

        console.log(`Inviando batch ${batchIndex + 1} di ${totalBatches}:`, {
            headingBatch,
            paragraphBatch,
        });

        const response = await fetch('http://127.0.0.1:5000/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headings: headingBatch, paragraphs: paragraphBatch }),
        });

        const simplifiedData = await response.json();
        if (simplifiedData.error) {
            console.error("Errore dal server Flask:", simplifiedData.error);
            return;
        }

        console.log(`Dati semplificati ricevuti per batch ${batchIndex + 1}:`, simplifiedData);

        // Inject content for this batch
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: injectSimplifiedContent,
            args: [simplifiedData, headingOffset, paragraphOffset],
        });

        // Update offsets
        headingOffset += headingBatch.length;
        paragraphOffset += paragraphBatch.length;
    }

    console.log("Tutti i batch completati.");
}

function extractPageContent() {
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.textContent.trim());
    const paragraphs = Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim());
    return { headings, paragraphs };
}

function injectSimplifiedContent(simplifiedContent, headingOffset, paragraphOffset) {
    // Inject updated headings in place
    if (simplifiedContent.headings) {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        simplifiedContent.headings.forEach((newHeading, index) => {
            const actualIndex = headingOffset + index;
            if (headings[actualIndex]) {
                headings[actualIndex].innerHTML = newHeading;
            }
        });
    }

    // Inject updated paragraphs in place
    if (simplifiedContent.paragraphs) {
        const paragraphs = Array.from(document.querySelectorAll('p'));
        simplifiedContent.paragraphs.forEach((newParagraph, index) => {
            const actualIndex = paragraphOffset + index;
            if (paragraphs[actualIndex]) {
                paragraphs[actualIndex].innerHTML = newParagraph;
            }
        });
    }
}

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
