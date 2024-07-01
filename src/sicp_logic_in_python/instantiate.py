from .unification import is_variable


def instantiate(
    expr,
    frame: dict,
):
    if is_variable(expr):
        return frame[expr]

    elif isinstance(expr, tuple):
        return tuple(instantiate(e, frame) for e in expr)

    elif isinstance(expr, list):
        return [instantiate(e, frame) for e in expr]

    return expr
