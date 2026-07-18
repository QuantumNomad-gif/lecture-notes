def search_segments(query: str, segments: list[dict]) -> list[dict]:
    """Returns segments whose text contains the query (case-sensitive)"""
    query_lower = query.lower()
    matches = []

    for segment in segments:
        if query_lower in segment["text"].lower():
            matches.append(segment)

    return matches