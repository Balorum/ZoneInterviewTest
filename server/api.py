from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# genai.configure(api_key="AIzaSyDuTjnfNZYz5y2QYWST9wfs8oS44I1z-yo")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get("query", "")
    response = model.generate_content(user_query)
    answer = response.text
    return jsonify({"answer": answer})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    zapier_url = "https://hooks.zapier.com/hooks/catch/22496933/20lagpr/"
    requests.post(zapier_url, json=data)
    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)