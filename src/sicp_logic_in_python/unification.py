from typing import Any


def is_variable(x) -> bool:
    return isinstance(x, str) and x.startswith("?")


def pattern_match(
    pattern,
    datum,
    frame: dict,
) -> dict | None:
    frame = frame.copy()

    if frame is None:
        return None

    if pattern == datum:
        return frame

    if is_variable(pattern):
        return extend_if_consistent(pattern, datum, frame)

    if isinstance(pattern, (list, tuple)) and isinstance(datum, (list, tuple)):
        if len(pattern) != len(datum):
            return None

        for p, d in zip(pattern, datum):
            frame = pattern_match(p, d, frame)
            if frame is None:
                return None

        return frame

    return None


def extend_if_consistent(
    var: str,
    dat: Any,
    frame: dict,
) -> dict | None:
    if var in frame:
        # If the variable is already bound to a value in the frame, then we need to check if the
        # bound value can be matched with the datum. E.g. if the frame is {"?x": ("f", "?y")},
        # and we are trying to match "?x" with ("f", "a"), then we need to check if "?y" can be
        # matched with "a".
        return pattern_match(frame[var], dat, frame)

    frame[var] = dat
    return frame
