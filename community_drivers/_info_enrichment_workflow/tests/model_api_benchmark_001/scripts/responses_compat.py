from __future__ import annotations

from typing import Any


def extract_output_text_compat(raw_response: dict[str, Any]) -> str:
    """Extract model text from multiple Responses API shapes.

    Backward compatibility policy:
    1. Keep the original top-level `output_text` path as the preferred path.
    2. Fall back to newer/alternate nested content shapes only if needed.
    """
    text = raw_response.get('output_text')
    if isinstance(text, str) and text.strip():
        return text

    for item in raw_response.get('output', []):
        if item.get('type') != 'message':
            continue
        for content in item.get('content', []):
            content_type = content.get('type')
            if content_type in {'output_text', 'text'}:
                candidate = content.get('text')
                if isinstance(candidate, str) and candidate.strip():
                    return candidate
            # Some wrappers may nest text under `content[x].text.value`.
            nested = content.get('text')
            if isinstance(nested, dict):
                candidate = nested.get('value')
                if isinstance(candidate, str) and candidate.strip():
                    return candidate

    content = raw_response.get('content')
    if isinstance(content, list):
        for item in content:
            if not isinstance(item, dict):
                continue
            candidate = item.get('text')
            if isinstance(candidate, str) and candidate.strip():
                return candidate
            if isinstance(candidate, dict):
                value = candidate.get('value')
                if isinstance(value, str) and value.strip():
                    return value

    return ''
