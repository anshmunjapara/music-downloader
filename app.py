from flask import Flask, request, jsonify
from search_yt import search_yt
import yt_dlp

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")

    if not query:
        return jsonify({"status": "error", "message": "Query is empty"})

    results = search_yt(query)
    return jsonify({"results": results})


@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")

    if not url:
        return jsonify({"status": "error", "message": "The URL is Empty"})

    return jsonify({"status": "success", "message": "Download completed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
