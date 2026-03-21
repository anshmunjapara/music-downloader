from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/download", methods=["POST"])
def download():
    url = (request.json.get("url"))

    if not url:
        return jsonify({"status": "error", "message": "The URL is Empty"})

    return jsonify({"status": "success", "message": "Download completed"})
