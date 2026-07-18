def search_segments(query: str, segments: list[dict]) -> list[dict]:
    """Returns segments whose text contains the query (case-insensitive).

    Deliberately a simple substring scan, not a real search index — at
    lecture scale (~150 segments) a linear scan is fast enough, and this
    keeps the pipeline provably correct before adding any complexity like
    fuzzy matching or ranking"""
    query_lower = query.lower()
    matches = []

    for segment in segments:
        if query_lower in segment["text"].lower():
            matches.append(segment)

    return matches