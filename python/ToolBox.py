from time import perf_counter_ns


def escape_string(string: str) -> str:
    try:
        out = string.encode('unicode_escape').decode('utf-8')
    except Exception as e:
        out = string
    return out


def time_print(string: str, ignore=True):
    if ignore:
        return
    time = perf_counter_ns()
    print(f"{time}: {string}")
