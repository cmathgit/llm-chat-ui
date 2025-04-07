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

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route(api_structure, methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
            
        # Handle ping request for connection check
        if user_message == 'ping':
            return jsonify({"response": "pong"}), 200

        try:
            response = model.generate_content(user_message)
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"error": f"AI Model Error: {str(e)}"}), 500
    
    except Exception as e:
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

