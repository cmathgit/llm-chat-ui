# llm-chat-ui
Various chat UIs for local and cloud LLMs

# Limitation of Liability Statement

For a complete Limitation of Liability Statement, please visit my [website](https://cmathgit.github.io/).

# Statement of Copyright Protection

For a complete Statement of Copyright Protection, please visit my [website](https://cmathgit.github.io/).


# AI Chat Interface with Text-to-Speech
README for [TTS](https://github.com/cmathgit/llm-chat-ui/cloud/tts/)

A modern web application that combines the power of Google's Gemini AI for chat interactions with ElevenLabs' text-to-speech capabilities. The application features a responsive dark-themed UI with real-time connection status and audio playback support.

## Features

- 🤖 Real-time chat interface with Gemini AI
- 🔊 Text-to-speech synthesis using ElevenLabs
- 🎨 Modern dark theme with purple accents
- 📊 Real-time connection status indicators
- 💬 Support for both text and audio responses
- 🔄 Automatic message history
- 📱 Responsive design for all devices

## Prerequisites

Before running the application, ensure you have:

1. Python 3.8 or higher installed
2. mpv media player installed and added to your system PATH
   - For Windows: [Download mpv](https://mpv.io/installation/) and add the mpv directory to your PATH
   - For Linux: `sudo apt install mpv` (Ubuntu/Debian) or equivalent
   - For macOS: `brew install mpv`
3. API keys for:
   - Google AI (Gemini)
   - ElevenLabs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm-chat-ui/cloud/tts
```

2. Install required Python packages:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the src directory with your API keys, port number, and API structure:
```env
GOOGLE_API_KEY=your_google_ai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
PORT_NUMBER=your_port_number_here
API_STRUCTURE=your_api_structure_here
```

3. Create a `config.js` file in the src/static directory with your API keys, port number, and API structure:
```js
const config = {
    API_URL: 'http://localhost:your_port_number_here/your_api_structure_here'
};
```

## Running the Application

### For Local Development & Testing
1.  Ensure you're in the `src` directory:
    ```bash
    cd src
    ```
2.  Start the Flask development server:
    ```bash
    python api.py
    ```
    *   **Development Server Note:** This command currently runs the server with `debug=False` directly using Flask's built-in server. While `debug=False` is safer than `debug=True`, the built-in server is **not suitable for production**. See **Production Deployment** instructions below. For iterative development where you want automatic reloading on code changes, you might temporarily switch back to `debug=True` in `api.py` (**local use only!**).

3.  Open your web browser and navigate to:
    ```
    http://localhost:your_port_number_here
    ```
    (Replace `your_port_number_here` with the value from your `.env` file).

### For Production Deployment (Recommended)
1.  **Install WSGI Servers:** Gunicorn (for Linux/macOS) and Waitress (for Windows) are recommended production servers. Add them to your `requirements.txt` and install:
    ```bash
    # Add 'gunicorn' and 'waitress' to requirements.txt if not already there
    pip install gunicorn waitress
    ```
    (Ensure your virtual environment is activated).

2.  **Navigate to the Source Directory:** Change your current directory to where `api.py` is located:
    ```bash
    cd src
    ```

3.  **Run using a WSGI Server:** Once inside the `src` directory, choose the command appropriate for your operating system:

    *   **On Linux or macOS (using Gunicorn):**
        ```bash
        gunicorn --workers 4 --bind 0.0.0.0:your_port_number api:app
        ```

    *   **On Windows (using Waitress):**
        ```cmd
        waitress-serve --listen=*:your_port_number --threads=4 api:app
        ```

    *   **Notes:**
        *   Replace `your_port_number` with your actual port number from the `.env` file.
        *   **Gunicorn:** Adjust `--workers 4` based on your server's resources (e.g., `2 * number_of_cpu_cores + 1`). `--bind 0.0.0.0` makes it network-accessible.
        *   **Waitress:** Adjust `--threads 4` based on your expected concurrency. `--listen=*` makes it network-accessible on all interfaces (IPv4/IPv6).
        *   `api:app`: Tells the server to find the Flask instance `app` in `api.py`. This works because you are running the command from the same directory as `api.py`.
        *   **Ensure `debug=False`:** It's crucial that the Flask app itself is not configured in debug mode internally when running in production.

4.  **Access:** Access the application via your server's IP address or domain name at the specified port. Consider using a reverse proxy like Nginx or Apache in front of your WSGI server for enhanced performance, security (HTTPS), and load balancing.

## Usage

### Basic Chat
- Type your message in the input field
- Press Enter or click "Send" to send the message
- View AI responses in the chat history

### Text-to-Speech
- Type your message
- Click "Send & Read" to send the message and hear the response
- Note: TTS responses are limited to 50 characters for optimal performance
- Audio files are saved in the `audio` directory with timestamps

## Directory Structure

```
src/
├── api.py              # Main Flask application
├── static/
│   ├── styles.css      # Application styling
│   └── script.js       # Frontend functionality
├── index.html          # Main web interface
├── requirements.txt    # Python dependencies
└── audio/             # Generated audio files (created automatically)
```

## Technical Details

### Backend
- Flask web server with CORS support
- Google Generative AI (Gemini) for chat responses
- ElevenLabs API for text-to-speech synthesis
- Automatic audio file management with timestamps

### Frontend
- Modern HTML5/CSS3 interface
- Vanilla JavaScript for interactivity
- WebSocket-like connection status monitoring
- SVG icons for better scaling
- Responsive design with flexbox

## Security Considerations & Best Practices

This section outlines important security aspects and best practices to consider when running or deploying this application. While the core codebase separates sensitive data like API keys, certain runtime configurations require careful attention.

*   **Critical: Debug Mode (`debug=True`)**
    *   **WARNING:** Never run this application with `debug=True` enabled in any environment accessible by others (including production). The Flask development server (run via `python api.py`) should not be used for production deployment.
    *   **Risk:** Debug mode exposes an interactive debugger allowing **arbitrary code execution**, a critical security vulnerability.
    *   **Recommendation:** Always use a production WSGI server like Gunicorn or uWSGI, and ensure the Flask application is configured with `debug=False`.

*   **CORS (Cross-Origin Resource Sharing)**
    *   **Configuration:** The application currently uses `flask_cors.CORS(app)`, allowing requests from any origin (`*`).
    *   **Reasoning:** Permissive for local development convenience.
    *   **Recommendation:** For production deployments, **restrict CORS** origins. Modify the `CORS(app)` call in `api.py` to specify allowed domains, for example: `CORS(app, origins=["http://yourdomain.com", "https://yourdomain.com"])`. Only allow origins from where your frontend is served.

*   **LLM Input Handling & Context Customization**
    *   **Input Sanitization:** The backend (`api.py`) performs basic input sanitization before sending data to the Google AI API:
        *   Removes leading/trailing whitespace from user messages.
        *   Enforces a maximum character limit to prevent overly large requests.
    *   **Character Limit:** The current maximum input length is set to **4000 characters**. This is defined by the `MAX_INPUT_LENGTH` variable in `api.py`. You can adjust this value if needed, but be mindful of potential API limitations or costs associated with very long inputs.
    *   **LLM Context (System Prompt):** The application prepends a system prompt to every user message to guide the AI's persona and response style. This prompt is defined in the `SYSTEM_PROMPT` variable near the top of `api.py`.
    *   **Customizing Context:** To change the AI's behavior, persona, or instructions, simply **modify the content of the `SYSTEM_PROMPT` string** within `api.py`. You can provide any instructions or context you prefer for the LLM.

*   **Inherent LLM Risks (Contextual)**
    *   Interacting with Large Language Models (LLMs) like Gemini carries inherent considerations:
        *   **Prompt Injection:** Maliciously crafted inputs could potentially manipulate the AI's behavior. Use caution, especially if modifying the `SYSTEM_PROMPT`.
        *   **Data Privacy:** Be mindful of the data sent to the API, especially if handling sensitive user information. Avoid sending private data.
        *   **API Costs:** Usage of the Google AI and ElevenLabs APIs incurs costs based on your interaction volume.
    *   These are characteristics of the AI services themselves, not specific flaws in this application's code, but important factors for any user running the application.

*   **Production Deployment (WSGI Server)**
    *   **Requirement:** Do not use the built-in Flask development server (`python api.py` or `app.run()`) for production. It's not designed for security, performance, or stability under load.
    *   **Recommendation:** Use a production-grade WSGI server like **Gunicorn** (for Linux/macOS) or **Waitress** (for Windows). Follow the **Production Deployment** steps under the "Running the Application" section.
    *   **Reverse Proxy:** Consider placing Nginx or Apache in front of your WSGI server to handle static files efficiently, manage HTTPS (SSL/TLS), and provide load balancing or caching.

*   **Debug Mode:** The application is configured to run with `debug=True` by default when executing `python 
api.py`. While convenient for local development (providing automatic reloading and detailed error pages), 
**do not run the application with debug mode enabled in a production or publicly accessible environment.** 
Debug mode can expose sensitive information and allow for arbitrary code execution if an error occurs. For 
deployment, ensure `debug=False` is set.
*   **CORS (Cross-Origin Resource Sharing):** The application uses `flask_cors.CORS(app)` to allow requests 
from any origin. This is necessary for the typical local setup where the `index.html` file might be opened 
directly in the browser (potentially seen as a different origin, like `file://`) and needs to communicate 
with the Flask server running on `localhost`. If deploying this application, you should configure CORS more 
restrictively to only allow requests from your frontend's actual domain.

By understanding these points, users can run and potentially deploy this application more securely.

## Troubleshooting

1. If mpv is not found:
   - Ensure mpv is installed
   - Add mpv to your system PATH
   - Restart your terminal/command prompt
   - Try running `mpv --version` to verify installation

2. If audio doesn't play:
   - Check if mpv is properly installed and in PATH
   - Verify your ElevenLabs API key is correct
   - Check the application logs for specific errors

3. If the chat doesn't connect:
   - Verify your Google AI API key
   - Check if the Flask server is running
   - Look for any CORS-related errors in browser console

## Contributing

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.