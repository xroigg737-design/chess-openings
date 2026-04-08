from flask import Flask, request, Response
import requests
import os

app = Flask(__name__, static_folder=".", static_url_path="")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/explain", methods=["POST"])
def explain():
    if not ANTHROPIC_API_KEY:
        return {"error": "API key no configurada al servidor"}, 500

    data = request.get_json()

    def stream():
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
            json=data,
            stream=True,
        )
        for chunk in resp.iter_content(chunk_size=None):
            yield chunk

    return Response(stream(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5020)
