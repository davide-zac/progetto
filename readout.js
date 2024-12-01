// Inject the read-aloud functionality into the current page
document.getElementById('readAloudBtn').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: enableParagraphReadAloud
    });
});

// Function to enable paragraph hover and read aloud
function enableParagraphReadAloud() {
    let playIcon = null; // Single instance of the play icon
    let currentUtterance = null;
    let readingParagraph = null;

    // Function to stop any ongoing speech
    const stopReading = () => {
        if (currentUtterance) {
            window.speechSynthesis.cancel();
            currentUtterance = null;
        }
        if (readingParagraph) {
            // Reset the icon for the currently reading paragraph
            if (playIcon) playIcon.textContent = '▶';
            readingParagraph = null;
        }
    };

    // Create the play icon dynamically
    const createPlayIcon = () => {
        const icon = document.createElement('span');
        icon.className = 'play-icon';
        icon.style.position = 'absolute';
        icon.style.cursor = 'pointer';
        icon.style.background = 'white';
        icon.style.border = '1px solid black';
        icon.style.borderRadius = '25%';
        icon.style.width = '30px';
        icon.style.height = '30px';
        icon.style.display = 'flex';
        icon.style.alignItems = 'center';
        icon.style.justifyContent = 'center';
        //icon.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.2)';
        icon.textContent = '▶'; // Play icon
        return icon;
    };

    // Ensure only one icon exists
    const ensureSinglePlayIcon = () => {
        if (playIcon) {
            playIcon.remove(); // Remove any existing icon
        }
        playIcon = createPlayIcon();
        document.body.appendChild(playIcon);
    };

    // Hover behavior for paragraphs
    document.querySelectorAll('p').forEach(paragraph => {
        paragraph.style.position = 'relative';
        paragraph.style.transition = 'background-color 0.2s ease';
        paragraph.addEventListener('mouseenter', () => {
            ensureSinglePlayIcon(); // Ensure only one icon is created
            paragraph.style.backgroundColor = 'lightyellow'; // Highlight paragraph

            const rect = paragraph.getBoundingClientRect();
            playIcon.style.top = `${window.scrollY + rect.top + rect.height - 20}px`;
            playIcon.style.left = `${window.scrollX + rect.right - 20}px`;
            playIcon.style.display = 'flex';

            playIcon.onclick = () => {
                if (readingParagraph === paragraph) {
                    stopReading(); // Stop if the same paragraph is clicked
                    playIcon.textContent = '▶'; // Reset to play icon
                } else {
                    stopReading(); // Stop any ongoing speech
                    currentUtterance = new SpeechSynthesisUtterance(paragraph.textContent);
                    currentUtterance.lang = 'it-IT'; // Change as needed
                    currentUtterance.rate = 1; // Normal speed
                    currentUtterance.pitch = 1; // Normal pitch
                    currentUtterance.onend = () => {
                        playIcon.textContent = '▶'; // Reset icon on finish
                        readingParagraph = null;
                    };
                    window.speechSynthesis.speak(currentUtterance);
                    readingParagraph = paragraph;
                    playIcon.textContent = '⏹'; // Change to stop icon
                }
            };
        });

        paragraph.addEventListener('mouseleave', () => {
            paragraph.style.backgroundColor = ''; // Remove highlight
            if (!playIcon.matches(':hover')) {
                setTimeout(() => {
                    playIcon.style.display = 'none'; }, 10000); // 2000 milliseconds = 2 seconds
                
                //playIcon.style.display = 'none'; // Hide the icon if not hovering over it
            }
        });
    });

    // Hide the icon when clicking elsewhere
    //document.addEventListener('click', (event) => {
    //    if (playIcon && !playIcon.contains(event.target)) {
    //        playIcon.style.display = 'none';
    //    }
    //});

    document.addEventListener('click', (event) => {
        if (playIcon && !playIcon.contains(event.target)) {
           setTimeout(() => {
               playIcon.style.display = 'none'; }, 2000); // 2000 milliseconds = 2 seconds
               }
           });
}

