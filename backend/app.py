from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from backend import config
from backend.indexer import load_transcript
from backend.search import search_segments

app = Flask(__name__)

# CORS enabled globally — needed because the frontend is opened as a local
# file:// page rather than served from this same origin, which the browser
# otherwise treats as a cross-origin request and blocks
CORS(app)

print(os.path.abspath(config.AUDIO_DIR))  # sanity check on startup, confirms
                                            # Flask is resolving paths correctly


@app.route("/lectures")
def list_lectures():
    """Returns list of available transcript names (without .json extension),
    so the frontend dropdown doesn't need lecture names hardcoded"""
    files = os.listdir(config.TRANSCRIPTS_DIR)
    names = [os.path.splitext(f)[0] for f in files if f.endswith(".json")]
    return jsonify(names)


@app.route("/search")
def search():
    """Thin HTTP wrapper around search_segments(), no search logic lives here"""
    lecture = request.args.get("lecture")
    query = request.args.get("q")

    if not lecture or not query:
        return jsonify({"error": "lecture and q parameters required"}), 400

    json_path = os.path.join(config.TRANSCRIPTS_DIR, f"{lecture}.json")
    if not os.path.exists(json_path):
        return jsonify({"error": "lecture not found"}), 404

    segments = load_transcript(json_path)
    results = search_segments(query, segments)
    return jsonify(results)


@app.route("/audio/<filename>")
def serve_audio(filename):
    """Serves the raw audio file so the browser's <audio> tag can play and
    seek it. mimetype is set explicitly since .m4a isn't reliably
    auto-detected, it's actually an MPEG-4 audio container, and without
    this the browser's Opaque Response Blocking rejects the response"""
    full_path = os.path.join(config.AUDIO_DIR, filename)
    print(f"Looking for: {os.path.abspath(full_path)}")
    print(f"Exists: {os.path.exists(full_path)}")
    return send_from_directory(config.AUDIO_DIR, filename, mimetype="audio/mp4")


if __name__ == "__main__":
    app.run(debug=True)