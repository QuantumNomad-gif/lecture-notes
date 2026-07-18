import json
import os
from backend import config

def save_transcript(audio_filename: str, segments: list[dict]) -> str:
    """Saves segments to a JSON file named after the source audio file.
    Returns the path it was saved to."""
    os.makedirs(config.TRANSCRIPTS_DIR, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(audio_filename))[0]
    output_path = os.path.join(config.TRANSCRIPTS_DIR, f"{base_name}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2)

    return output_path

def load_transcript(json_path: str) -> list[dict]:
    """Loads segments back from a saved JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)