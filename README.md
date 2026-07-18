# Lecture Notes Search

Turn a lecture recording into a searchable transcript, type a word, jump straight
to the timestamp it was said, click to seek and play from that moment.

**Status: V1, core pipeline working end-to-end on a single lecture.**

## The problem

Lecture recordings are useful but unsearchable. If you remember a lecturer said
something about a specific topic, finding *where* in a 50-minute recording means
scrubbing through audio by ear. This tool turns that into a text search.

## How it works

1. **Transcribe**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
   (local, CPU-only, `int8` quantized `base` model) converts a lecture recording
   into timestamped text segments.
2. **Index**: segments are saved to disk as JSON, so transcription only needs
   to run once per recording.
3. **Search**: a query returns every matching segment, in chronological order,
   with start/end timestamps.
4. **Play**: a browser frontend lets you click a search result and the audio
   player seeks straight to that moment.

## Architecture

```
lecture-notes/
├── backend/
│   ├── transcriber.py   # audio file -> timestamped segments (faster-whisper)
│   ├── indexer.py       # segments -> saved JSON, and back
│   ├── search.py        # query -> matching segments
│   ├── app.py           # Flask routes wiring the above together
│   └── config.py        # model size, paths
├── frontend/
│   └── index.html       # single-page UI: dropdown, search box, results, audio player
├── audio/                # lecture recordings (gitignored, see note below)
└── transcripts/          # generated JSON transcripts (gitignored, see note below)
```

Each backend module was built and tested standalone before being wired together,
`transcriber.py` proven on a real lecture file first, then `indexer.py`'s
save/load round-trip, then `search.py` against a saved transcript, and only then
the Flask/HTML layer on top of already-working functions.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Drop a lecture recording (`.mp3`, `.m4a`, or most common audio formats) into `audio/`.

```bash
python -m backend.app
```

Open `frontend/index.html` directly in a browser.

## Note on audio/transcripts

This repo doesn't include sample lecture audio or transcripts. The recordings
used during development belong to lecture content I don't have distribution
rights for, so `audio/` and `transcripts/` are gitignored (structure kept via
`.gitkeep`). Drop your own recording into `audio/` to test the pipeline.

## Tech

- Python (Flask, faster-whisper)
- Vanilla HTML/CSS/JS frontend (no framework, kept deliberately simple)
- JSON for transcript storage (no database — not needed at this scale)

## What's not built yet (V2 candidates)

- File upload from the browser (currently points at whatever's already in `audio/`/`transcripts/`)
- Batch processing / searching across multiple lectures at once
- Visual polish and accessibility pass
- Fuzzy/partial matching in search (currently exact substring match)