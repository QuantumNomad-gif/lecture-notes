from faster_whisper import WhisperModel
from backend import config

def transcribe(audio_path: str) -> list[dict]:
    """Runs local transcription on an audio file and returns timestamped segments

    Returns list of {start, end, text} dicts, one per spoken segment"""

    # NOTE: model is reloaded on every call — fine for one-off testing, but
    # this is the thing to fix (load once, reuse) before batch-processing
    # multiple lectures or wiring this into a long-running Flask process
    # TODO: Fix multiple instances
    model = WhisperModel(config.MODEL_SIZE, device=config.DEVICE, compute_type=config.COMPUTE_TYPE)

    # segments is a generator — nothing actually runs until it's iterated
    # below. info holds metadata like detected language, useful as a sanity
    # check that the audio wasn't misdetected as a different language
    segments, info = model.transcribe(audio_path)

    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    return result