# sicp-logic-in-python

A Python implementation of the logic programming language described in the book "Structure and Interpretation of Computer Programs" (SICP).

The implementation exploits the Python's generator feature to implement the logic programming language.

We exclude dotted-tail patterns from the original language and indexing of assertions and rules.

## Usage

```python
pip install -e .
```

```python
from sicp_logic_in_python import query, MemoryDB

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
>>> [('parent', 'Homer', 'Bart'), ('parent', 'Marge', 'Bart')]
```

# Resources

- [SICP Chapter 4.4](https://sarabander.github.io/sicp/html/4_002e4.xhtml)
- [jdormit/sicp-logic](https://github.com/jdormit/sicp-logic)
