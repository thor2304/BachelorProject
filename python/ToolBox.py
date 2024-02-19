def escape_string(string: str) -> str:
    return string.encode('unicode_escape').decode('utf-8')