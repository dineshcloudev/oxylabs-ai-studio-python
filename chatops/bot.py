from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/slack', methods=['POST'])
def slack_bot():
    text = request.form.get('text')

    if "status" in text:
        return "AI Studio is running ✅"

    if "pods" in text:
        return "Check Kubernetes pods using kubectl"

    if "search" in text:
        return "Search feature coming soon 🔍"

    return "Unknown command"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
