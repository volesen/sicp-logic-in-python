from sicp_logic_in_python.unification import extend_if_possible, unify


def test_unify():
    assert unify(
        ("?x", 2, "?z"),
        (1, "?y", 3),
        frame={},
    ) == {
        "?x": 1,
        "?y": 2,
        "?z": 3,
    }

    assert unify(
        ("?x", "?x"),
        ("?y", "?y"),
        frame={},
    ) == {
        "?x": "?y",
    }


def test_extend_if_possible():
    assert extend_if_possible(
        "?x",
        ("f", "a"),
        frame={"?x": ("f", "?y")},
    ) == {
        "?x": ("f", "?y"),
        "?y": "a",
    }

    assert (
        extend_if_possible(
            "?x",
            ("f", "b"),
            frame={"?x": ("f", "?y"), "?y": "a"},
        )
        is None
    )
