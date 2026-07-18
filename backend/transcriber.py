from faster_whisper import WhisperModel
from backend import config

def transcribe(audio_path: str) -> list[dict]:
    """Returns list of {start, end, text} segments."""
    model = WhisperModel(config.MODEL_SIZE, device=config.DEVICE, compute_type=config.COMPUTE_TYPE) 
    # TODO: Fix multiple instances
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