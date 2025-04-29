# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from run_multi_agent import run_multi_agent

app = Flask(__name__)
CORS(app)  # 解決前後端不同源的問題

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input = data.get('user_input')
    response = run_multi_agent(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
