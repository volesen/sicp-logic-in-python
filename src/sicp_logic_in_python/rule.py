from .unification import is_variable


class RuleCounter:
    def __init__(self):
        self.count = 0

    def new_rule_application(self):
        self.count += 1
        return self.count


rule_counter = RuleCounter()


def rename_variables(
    rule: tuple,
):
    rule_application_id = rule_counter.new_rule_application()

    def tree_walk(expr):
        if is_variable(expr):
            return f"{expr}_{rule_application_id}"

        if isinstance(expr, tuple):
            return tuple(tree_walk(x) for x in expr)

        if isinstance(expr, list):
            return [tree_walk(x) for x in expr]

        return expr

    return tuple(tree_walk(x) for x in rule)
