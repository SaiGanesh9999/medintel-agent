from collections import Counter
from time import perf_counter


class Metrics:
    """
    Minimal metrics helper: counts + timings.
    """

    def __init__(self):
        self.counters = Counter()
        self.timings = []

    def inc(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def time_block(self, name: str):
        start = perf_counter()

        class _Timer:
            def __enter__(self_inner):
                return None

            def __exit__(self_inner, exc_type, exc_val, exc_tb):
                duration = perf_counter() - start
                self.timings.append((name, duration))

        return _Timer()
