import os

MODEL_SIZE = "base"       # start here, step up to "small" only if accuracy is bad
DEVICE = "cpu"            # explicit, since you're checking this stays lightweight
COMPUTE_TYPE = "int8"     # fastest CPU inference mode faster-whisper supports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")