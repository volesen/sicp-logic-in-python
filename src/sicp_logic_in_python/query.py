from typing import Callable, Iterable

from .db import DB
from .instantiate import instantiate
from .rule import rename_variables
from .unification import unify


def query(
    query,
    db: DB,
):
    for frame in qeval(query, [{}], db):
        yield instantiate(query, frame)


def qeval(
    query,
    frames: Iterable[dict],
    db: DB,
):
    match query:
        case ["not", *operands]:
            yield from negate(operands, frames, db)

        case ["or", *disjuncts]:
            yield from disjoin(disjuncts, frames, db)

        case ["and", *conjuncts]:
            yield from conjoin(conjuncts, frames, db)

        case ["python-value", predicate, *args]:
            yield from python_value(predicate, args, frames, db)

        case (query,):
            yield from simple_query(query, frames, db)

        case _:
            yield from simple_query(query, frames, db)


def negate(
    operands: Iterable[tuple],
    frames: Iterable[dict],
    db: DB,
) -> Iterable[dict]:
    for frame in frames:
        for extended_frame in qeval(operands, [frame], db):
            break
        else:
            yield frame


def conjoin(
    conjuncts: Iterable[tuple],
    frames: Iterable[dict],
    db: DB,
) -> Iterable[dict]:
    for conjunct in conjuncts:
        frames = qeval(conjunct, frames, db)

    return frames


def disjoin(
    disjuncts: Iterable[tuple],
    frames: Iterable[dict],
    db: DB,
) -> Iterable[dict]:
    for frame in frames:
        for disjunct in disjuncts:
            yield from qeval(disjunct, [frame], db)


def simple_query(
    pattern: tuple,
    frames: Iterable[dict],
    db: DB,
) -> Iterable[dict]:
    for frame in frames:
        yield from find_assertions(pattern, frame, db)
        yield from apply_rules(pattern, frame, db)


def find_assertions(
    pattern,
    frame: dict,
    db: DB,
) -> Iterable[dict]:
    for assertion in db.fetch_assertions(pattern, frame):
        extended_frame = unify(assertion, pattern, frame)
        if extended_frame is not None:
            yield extended_frame


def apply_rules(
    pattern,
    frame: dict,
    db: DB,
) -> Iterable[dict]:
    for rule in db.fetch_rules(pattern, frame):
        yield from apply_rule(pattern, rule, frame, db)


def apply_rule(
    pattern,
    rule: tuple,
    frame: dict,
    db: DB,
) -> Iterable[dict]:
    conclusion, body = rename_variables(rule)

    extended_frame = unify(conclusion, pattern, frame)
    if extended_frame is not None:
        yield from qeval(body, [extended_frame], db)


def python_value(
    predicate: Callable,
    args: Iterable,
    frames: Iterable[dict],
    db: DB,
) -> Iterable[dict]:
    for frame in frames:
        if predicate(*instantiate(args, frame)):
            yield frame
