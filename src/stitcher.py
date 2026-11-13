import itertools
from dataclasses import dataclass


@dataclass
class BatchWindow:
    stream_id: str
    start_seq: int
    end_seq: int

    def span(self) -> int:
        return self.end_seq - self.start_seq


def stitch(windows: list[BatchWindow]) -> list[BatchWindow]:
    """Merge overlapping windows belonging to the same stream."""
    merged = []
    for window in sorted(windows, key=lambda w: (w.stream_id, w.start_seq)):
        if merged and merged[-1].stream_id == window.stream_id and window.start_seq <= merged[-1].end_seq:
            merged[-1].end_seq = max(merged[-1].end_seq, window.end_seq)
        else:
            merged.append(window)
    return merged
