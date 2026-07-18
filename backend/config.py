import os

# Model settings; tuned for CPU-only
MODEL_SIZE = "base"       # "base" gave clean, accurate transcripts on real lecture
                           # audio in testing — "tiny" would be faster but wasn't
                           # needed since base already runs in reasonable time on CPU
DEVICE = "cpu"
COMPUTE_TYPE = "int8"      # int8 quantization is the key setting for CPU speed
                           # trades a little precision for meaningfully faster inference

# Compute paths relative to this file's location (not the current working
# directory) so the app works correctly no matter where it's launched from
# This fixed a real bug: send_from_directory silently 404s if AUDIO_DIR
# is a relative path that doesn't match Flask's internal root resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")