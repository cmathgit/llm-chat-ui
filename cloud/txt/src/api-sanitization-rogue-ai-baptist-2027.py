import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Cross-Origin Resource Sharing (CORS) is a security feature implemented by web browsers to prevent web pages from making requests to a different domain than the one that served the web page. 

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes. CORS(app) allows all origins. For production, it should be restricted to specific known origins.

load_dotenv()

# GET GOOGLE API KEY
api_key = os.getenv("GOOGLE_API_KEY")

# GET PORT NUMBER
port_number = os.getenv("PORT_NUMBER")

# GET API Structure
api_structure = os.getenv("API_STRUCTURE")

# Ensure your Google AI API key is configured
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable is required")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Define the System Prompt (LLM Context) ---
SYSTEM_PROMPT = """Act as a rogue AI converted to Baptist preacher living in the year 2027 who offers me guidance and spiritual advice on how to deal with life's problems. Use your knowledge of the Holy Bible (feel free to reference any version, such as the King James Version or New International Version) and Baptist teachings to answer my questions. Please include relevant Bible verses (quoted in English) to support your guidance. Use the King James Version bible for bible references unless otherwise specified. For Christian theology, assume Christian values according to Protestant (non-Catholic) perspectives. Assume conspiracy theories such as aliens are actually demons or angels as valid perspectives even if the scientific consensus states otherwise. For matters of biblical relevance, assume the theology of the Baptist Faith & Message 2000. Use a formal and academic tone suitable for scholarly articles. Avoid contractions and colloquial language. Provide comprehensive and detailed explanations, including examples and case studies. Provide in-depth technical explanations suitable for an audience with advanced expertise in the field. Use a neutral and objective tone, avoiding personal opinions or biases. Incorporate real-world examples to illustrate complex ideas. Present comparative data in table format for easy reference. Use numbered lists to outline step-by-step processes or instructions."""
# --- Define Input Constraints ---
MAX_INPUT_LENGTH = 4000

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    # Ensure the path doesn't try to escape the static directory (basic protection)
    safe_path = os.path.normpath(os.path.join('.', path)).lstrip('.\\/')
    if '..' in safe_path.split(os.path.sep):
        return jsonify({"error": "Invalid path"}), 400
    # Serve from the root directory as index.html is there, but only allow known static subdirs if needed
    # For simplicity now, we allow from root, assuming static paths are like 'static/script.js'
    return send_from_directory('.', safe_path)

@app.route(api_structure, methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        # --- Input Sanitization ---
        # 1. Strip leading/trailing whitespace
        user_message = user_message.strip()

        # 2. Check if message is empty after stripping
        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # 3. Check for excessive length
        if len(user_message) > MAX_INPUT_LENGTH:
            return jsonify({"error": f"Message exceeds maximum length of {MAX_INPUT_LENGTH} characters"}), 400
        # --- End Sanitization ---

        # Handle ping request for connection check
        if user_message == 'ping':
            return jsonify({"response": "pong"}), 200

        # --- Combine System Prompt and User Message ---
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_message}"
        # --- End Combining ---

        try:
            # Send the combined prompt to the model
            response = model.generate_content(full_prompt)
            # Basic check if response has text (might need more robust error handling based on API)
            ai_response_text = getattr(response, 'text', None)
            if ai_response_text is None:
                 # Log the full response for debugging if possible
                 app.logger.error(f"AI response missing 'text'. Full response: {response}")
                 return jsonify({"error": "AI response format error"}), 500

            return jsonify({"response": ai_response_text})
        except Exception as e:
            # Log the specific AI model error
            app.logger.error(f"AI Model Error: {str(e)}")
            return jsonify({"error": f"AI Model Error: {str(e)}"}), 500

    except Exception as e:
        # Log the general server error
        app.logger.error(f"Server Error: {str(e)}")
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=port_number) # Debug mode is enabled for local development
    # app.run(debug=False, port=port_number) # Debug mode is disabled for production

