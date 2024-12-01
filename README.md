# ReadIT: An IA google chrome extension helping people with dyslexia 

This is the repo for the demo of ReadIT. ReadIT is a google chrome extension that leverages Llama, the opensource LLM model from Meta, to process the text of any website and help dyslexic people in reading.

## Getting Started

To begin, you need to download or clone this repository to your local machine.

### Cloning the Repository

1. Open your terminal and run the following command:
   ```bash
   git clone https://github.com/davide-zac/ReadIT.git
2. Navigate to the cloned directory:
   ```bash
   cd ReadIT
   
## Installation Requirements

Before running the extension and the server, ensure you have the required dependencies installed. These are listed in the `requirements.txt` file.

### Steps to Install Requirements

1. Make sure you have Python installed on your system.
2. Install the dependencies by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   
## Running the Server
To test the extension, the server must be running. Use the following steps to start the server:

1. Navigate to the project directory where app.py is located.
2. Start the server with:
    ```bash
    python app.py
3. Ensure the server is running before testing the extension.

## Loading the Extension in Chrome

To test the extension, follow these steps to load it into Chrome:

1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** by toggling the switch in the top-right corner.
3. Click on **Load unpacked**.
4. Select the folder containing the Chrome extension files (the folder where `manifest.json` is located).
5. The extension will now appear in the list of installed extensions.

## Testing the Extension

1. Ensure the server is running (see "Running the Server").
2. Use the extension in Chrome and verify its functionality.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

