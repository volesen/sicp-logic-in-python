from sicp_logic_in_python import query, MemoryDB


def test_readme_example():
    db = MemoryDB()

    db.add_assertion(("father", "Homer", "Bart"))
    db.add_assertion(("father", "Homer", "Lisa"))
    db.add_assertion(("father", "Homer", "Maggie"))
    db.add_assertion(("mother", "Marge", "Bart"))
    db.add_assertion(("mother", "Marge", "Lisa"))
    db.add_assertion(("mother", "Marge", "Maggie"))

    db.add_rule(
        (
            ("parent", "?x", "?y"),
            [
                "or",
                ("father", "?x", "?y"),
                ("mother", "?x", "?y"),
            ],
        )
    )

    query(("parent", "?x", "Bart"), db)

    assert list(query(("parent", "?x", "Bart"), db)) == [
        ("parent", "Homer", "Bart"),
        ("parent", "Marge", "Bart"),
    ]
