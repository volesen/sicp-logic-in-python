from typing import Iterable


class DB:
    def add_assertion(self, assertion: tuple):
        raise NotImplementedError

    def fetch_assertions(self, pattern, frame) -> Iterable[tuple]:
        raise NotImplementedError

    def add_rule(self, rule: tuple):
        raise NotImplementedError

    def fetch_rules(self, pattern, frame) -> Iterable[tuple]:
        raise NotImplementedError


class MemoryDB(DB):
    def __init__(self):
        self.assertions = []
        self.rules = []

    def add_assertion(self, assertion: tuple):
        self.assertions.append(assertion)

    def fetch_assertions(self, pattern, frame) -> Iterable[tuple]:
        return self.assertions

    def add_rule(self, rule: tuple):
        self.rules.append(rule)

    def fetch_rules(self, pattern, frame) -> Iterable[tuple]:
        return self.rules
