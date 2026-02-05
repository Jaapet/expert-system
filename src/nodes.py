class FactNode:

    def __init__(self, name):
        self.name = name
        self.value = False # Default
        self.is_true_by_default = False
        self.implying_rules = [] # List of RuleNodes that conclude this fact

    def __repr__(self):
        return f"Fact({self.name}, Val:{self.value})"


class RuleNode:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Rule({self.left} => {self.right})"
