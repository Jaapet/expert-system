class KnowledgeBase:

    def __init__(self):
        # List to store all rules.
        # Each rule is a dict: {'left': [...], 'right': [...]}
        self.rules = []

        # Dict to store facts facts.
        # Key: 'A', Value: True/False/None
        self.facts = {}

        # A set for all unique symbols from rules
        self.symbols = set()


    def add_rule(self, left, operator, right):
        """
        Adds a rule to the database.
        Handles the split of Biconditional (<=>) rules automatically.
        """
        # Get symbols from rule
        for token in left + right:
            if token.isupper() and len(token) == 1:
                self.symbols.add(token)

        # MANDATORY: Standard Implication (=>)
        if operator == '=>':
            self.rules.append({'left': left, 'right': right})

        # BONUS: Biconditional (<=>) 
        # "A <=> B" = "A => B" AND "B => A"
        elif operator == '<=>':
            self.rules.append({'left': left, 'right': right}) # Forward
            self.rules.append({'left': right, 'right': left}) # Backward


    def set_initial_facts(self, facts_str):
        """
        Parses the initial facts string (e.g., "=ABC").
        Sets these to True. All others default to False.
        """
        # Get symbols
        for symbol in self.symbols:
            self.facts[symbol] = False

        # Set initial facts to True (ex: "=ABC")
        clean_facts = facts_str.replace('=', '').strip()
        for char in clean_facts:
            if char.isupper():
                self.facts[char] = True

    # More readable print
    def __str__(self):
        return f"Facts: {self.facts}\nRules: {len(self.rules)}"


# # Test
# if __name__ == "__main__":
#     kb = KnowledgeBase()
    
#     # Simulate adding rules from parser
#     # Rule 1: A + B => C
#     kb.add_rule(['A', 'B', '+'], '=>', ['C'])
    
#     # Rule 2 (Bonus): D <=> E (Stored as D=>E and E=>D)
#     kb.add_rule(['D'], '<=>', ['E'])
    
#     # Simulate setting initial facts
#     kb.set_initial_facts("=AC") 
    
#     print(kb)
#     # Expected:
#     # Facts: {'A': True, 'B': False, 'C': True, 'D': False, 'E': False}
#     # Rules: 3 (1 standard + 2 from '<=>')
