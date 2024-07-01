from typing import Any


def is_variable(x) -> bool:
    return isinstance(x, str) and x.startswith("?")


def unify(
    pattern1,
    pattern2,
    frame: dict,
) -> dict | None:
    if pattern1 == pattern2:
        return frame

    if is_variable(pattern1):
        return extend_if_possible(pattern1, pattern2, frame)

    if is_variable(pattern2):
        return extend_if_possible(pattern2, pattern1, frame)

    if isinstance(pattern1, (list, tuple)) and isinstance(pattern2, (list, tuple)):
        if len(pattern1) != len(pattern2):
            return None

        for p1, p2 in zip(pattern1, pattern2):
            frame = unify(p1, p2, frame)
            if frame is None:
                return None

        return frame
    
    return None


def extend_if_possible(
    var: str,
    val: Any,
    frame: dict,
) -> dict | None:
    if var in frame:
        return unify(frame[var], val, frame)

    if is_variable(val) and val in frame:
        return unify(var, frame[val], frame)

    if depends_on(val, var, frame):
        return None

    frame = frame.copy()
    frame[var] = val
    return frame


def depends_on(expr, var, frame) -> bool:
    if expr == var:
        return True

    if expr in frame:
        return depends_on(frame[expr], var, frame)

    if isinstance(expr, (list, tuple)):
        return any(depends_on(x, var, frame) for x in expr)

    return False
