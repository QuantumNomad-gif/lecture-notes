from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from backend import config
from backend.indexer import load_transcript
from backend.search import search_segments

app = Flask(__name__)
CORS(app)

print(os.path.abspath(config.AUDIO_DIR))

@app.route("/lectures")
def list_lectures():
    """Returns list of available transcript names (without .json extension)"""
    files = os.listdir(config.TRANSCRIPTS_DIR)
    names = [os.path.splitext(f)[0] for f in files if f.endswith(".json")]
    return jsonify(names)

@app.route("/search")
def search():
    """Expects ?lecture=Elec_4a&q=magnetic+force"""
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
    full_path = os.path.join(config.AUDIO_DIR, filename)
    print(f"Looking for: {os.path.abspath(full_path)}")
    print(f"Exists: {os.path.exists(full_path)}")
    return send_from_directory(config.AUDIO_DIR, filename, mimetype="audio/mp4")

if __name__ == "__main__":
    app.run(debug=True)