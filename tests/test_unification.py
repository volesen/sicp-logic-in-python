from sicp_logic_in_python.unification import pattern_match, extend_if_consistent


def test_pattern_match(): ...


def test_extend_if_consistent():
    assert extend_if_consistent(
        "?x",
        ("f", "a"),
        frame={"?x": ("f", "?y")},
    ) == {
        "?x": ("f", "?y"),
        "?y": "a",
    }

    # Negative test
    assert (
        extend_if_consistent(
            "?x",
            ("f", "b"),
            frame={"?x": ("f", "?y"), "?y": "a"},
        )
        is None
    )
