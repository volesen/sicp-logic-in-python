import pytest
from sicp_logic_in_python.db import MemoryDB
from sicp_logic_in_python.query import qeval
from sicp_logic_in_python.instantiate import instantiate


@pytest.fixture
def db():
    db = MemoryDB()

    db.add_assertion(("male", "jack"))
    db.add_assertion(("male", "oliver"))
    db.add_assertion(("male", "ali"))
    db.add_assertion(("male", "james"))
    db.add_assertion(("male", "simon"))
    db.add_assertion(("male", "harry"))
    db.add_assertion(("female", "helen"))
    db.add_assertion(("female", "sophie"))
    db.add_assertion(("female", "jess"))
    db.add_assertion(("female", "lily"))

    db.add_assertion(("parent_of", "jack", "jess"))
    db.add_assertion(("parent_of", "jack", "lily"))
    db.add_assertion(("parent_of", "helen", "jess"))
    db.add_assertion(("parent_of", "helen", "lily"))
    db.add_assertion(("parent_of", "oliver", "james"))
    db.add_assertion(("parent_of", "sophie", "james"))
    db.add_assertion(("parent_of", "jess", "simon"))
    db.add_assertion(("parent_of", "ali", " simon"))
    db.add_assertion(("parent_of", "lily", "harry"))
    db.add_assertion(("parent_of", "james", "harry"))

    db.add_rule(
        (
            ("father_of", "?x", "?y"),
            [
                "and",
                ("male", "?x"),
                ("parent_of", "?x", "?y"),
            ],
        ),
    )

    db.add_rule(
        (
            ("mother_of", "?x", "?y"),
            [
                "and",
                ("female", "?x"),
                ("parent_of", "?x", "?y"),
            ],
        )
    )

    return db


def test_simple_query(db):
    assert {
        frame["?x"]
        for frame in qeval(
            ("male", "?x"),
            [{}],
            db,
        )
    } == {
        "jack",
        "oliver",
        "ali",
        "james",
        "simon",
        "harry",
    }


def test_disjoin_query(db):
    assert {
        frame["?x"]
        for frame in qeval(
            ["or", ("male", "?x"), ("female", "?x")],
            [{}],
            db,
        )
    } == {
        "jack",
        "oliver",
        "ali",
        "james",
        "simon",
        "harry",
        "helen",
        "sophie",
        "jess",
        "lily",
    }


def test_negate_query(db):
    assert {
        frame["?x"]
        for frame in qeval(
            ("male", "?x"),
            [
                {
                    "?x": "jack",
                },
                {
                    "?x": "helen",
                },
            ],
            db,
        )
    } == {"jack"}

    assert {
        frame["?x"]
        for frame in qeval(
            ["not", ("male", "?x")],
            [
                {
                    "?x": "jack",
                },
                {
                    "?x": "helen",
                },
            ],
            db,
        )
    } == {"helen"}


def test_compound_query(db):
    assert list(
        qeval(
            [
                "and",
                ("parent_of", "?x", "harry"),
                ("male", "?x"),
            ],
            [{}],
            db,
        )
    ) == [
        {"?x": "james"},
    ]


def test_rule_query(db):
    (frame,) = list(
        qeval(
            ("father_of", "?x", "harry"),
            [{}],
            db,
        )
    )

    assert instantiate("?x", frame) == "james"


def test_python_value_query(db):
    assert (
        len(
            list(
                qeval(
                    [
                        "and",
                        ("parent_of", "?x", "harry"),
                        ("parent_of", "?y", "harry"),
                    ],
                    [{}],
                    db,
                )
            )
        )
        == 4
    )

    def not_equal(x, y):
        return x != y

    assert (
        len(
            list(
                qeval(
                    [
                        "and",
                        ("parent_of", "?x", "harry"),
                        ("parent_of", "?y", "harry"),
                        ["python-value", not_equal, "?x", "?y"],
                    ],
                    [{}],
                    db,
                )
            )
        )
        == 2
    )
