from flask import Flask, request, jsonify, render_template
from google.cloud import storage
import os

app = Flask(__name__)

BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "backend-anirudh21")
MAX_FILE_SIZE_MB = int(os.environ.get("MAX_FILE_SIZE_MB", 5))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
storage_client = storage.Client()


# Universal CORS headers
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"  # allow all origins
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/")
def home():
    return render_template("index.html")  # Serve your HTML from here


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE_BYTES:
        return (
            jsonify({"error": f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB"}),
            400,
        )

    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        blob.make_public()
        return (
            jsonify(
                {"message": "File uploaded successfully", "file_url": blob.public_url}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Failed to upload file to GCS: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
