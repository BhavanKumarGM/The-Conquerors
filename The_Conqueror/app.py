from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Chatbot Server is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    """Receives text input, processes it with AI, and returns a response."""
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    if user_message.lower() == "exit":
        return jsonify({"response": "Goodbye!"})

    # AI response from Ollama (Llama 2 Model)
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": user_message}])
    ai_response = response['message']['content']

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
