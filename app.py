from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # السماح لكل المصادر بالوصول إلى API

API_KEYS = {
    "deepseek": "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",
    "gemini": "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",
    "gpt": "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",
    "llama": "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"
}

MODELS = {
    "deepseek": "deepseek/deepseek-r1:free",
    "gemini": "google/gemini-2.0-flash-thinking-exp:free",
    "gpt": "openai/gpt-3.5-turbo",
    "llama": "meta-llama/llama-2-13b-chat"
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_chatbot_response(model_name, user_input):
    """ يرسل السؤال إلى API chatbot معين ويعيد الإجابة """
    headers = {
        "Authorization": f"Bearer {API_KEYS[model_name]}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODELS[model_name],
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 3000
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}: {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("question", "")

    responses = {}
    for bot in API_KEYS.keys():
        try:
            responses[bot] = get_chatbot_response(bot, user_input)
        except Exception as e:
            responses[bot] = f"Error: {str(e)}"
    
    return jsonify(responses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

