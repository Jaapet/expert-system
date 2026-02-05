class InferenceEngine:

    def __init__(self, kb):

        self.kb = kb
        # Stack to store already seen (avoid loops : A -> B -> A)
        self.recursion_stack = set()


    def _check_conclusion(self, right_rpn, query):
        """
        Analyzes the right to see what it says about the query.
        Returns: True (implies query is True), False (implies query is False), None (Undetermined)
        """
        # Simple case: right is just the query ['B']
        if len(right_rpn) == 1 and right_rpn[0] == query:
            return True
            
        # Negation case: right is ['B', '!']
        if len(right_rpn) == 2 and right_rpn[0] == query and right_rpn[1] == '!':
            return False

        # If 'query' appears in an OR block in right (B | C), it is Undetermined.
        if '|' in right_rpn:
            return None # OR in conclusion is ambiguous

        # If 'query' appears in an AND block (B + !C) with '!'.
        if '!' in right_rpn:
             # Check if 'query' is the one being negated
             try:
                 idx = right_rpn.index(query)
                 # Check if next token is '!'
                 if idx + 1 < len(right_rpn) and right_rpn[idx+1] == '!':
                     return False
             except ValueError:
                 pass

        # If 'query' appears in an AND block (B + C), it is True.
        return True # Default for AND chains


    def _apply_operator(self, stack, op):
        
        if op == '!': # NOT
            val = stack.pop()
            # !True = False, !False = True, !None = None
            if val is None: stack.append(None)
            else: stack.append(not val)
            return

        right = stack.pop()
        left = stack.pop()

        if op == '+': # AND
            # True + True = True
            # False + anything = False
            # True + None = None
            if left is False or right is False:
                stack.append(False)
            elif left is None or right is None:
                stack.append(None)
            else:
                stack.append(True)

        elif op == '|': # OR
            # True | anything = True
            # False | False = False
            # False | None = None
            if left is True or right is True:
                stack.append(True)
            elif left is None or right is None:
                stack.append(None)
            else:
                stack.append(False)

        elif op == '^': # XOR
            # True ^ False = True
            # True ^ True = False
            # None ^ anything = None
            if left is None or right is None:
                stack.append(None)
            else:
                stack.append(left != right)


    def eval_rpn(self, expression):
        """
        Evaluates an RPN list recursively (e.g. ['A', 'B', '+'])
        Returns: True, False, or None
        """
        stack = []

        for token in expression:
            if token.isupper():
                # Solve the symbol
                result = self.solve(token)
                stack.append(result)

            elif token in ['!', '+', '|', '^']:
                self._apply_operator(stack, token)

        return stack[0] if stack else False


    def solve(self, query):
        """
        Determines the truth value of a query symbol (True, False, or None).
        """
        # Retrieve the node corresponding to the query
        node = self.kb.get_node(query)

        # Case: loop detection
        if query in self.recursion_stack:
            return False 

        # Case: check initial fact
        if node.is_true_by_default:
            return True

        self.recursion_stack.add(query)

        # Get rules that imply query
        query_rules = node.implying_rules

        is_true = False
        is_false = False
        is_undetermined = False

        # Evaluate rules
        for rule in query_rules:
            # Evaluate left recursively
            left_result = self.eval_rpn(rule.left)

            # If LEFT is True, check right
            if left_result is True:
                # Check how 'query' is used in right.
                # Standard: A => B (Imply B is True)
                # Negation: A => !B (Imply B is False)
                # Complex: A => B + C (Imply B is True)
                # Ambiguous: A => B | C (B is Undetermined)

                result = self._check_conclusion(rule.right, query)

                if result is True:
                    is_true = True
                elif result is False:
                    is_false = True
                elif result is None:
                    is_undetermined = True

        self.recursion_stack.remove(query)

        if is_true and is_false:
            raise ValueError(f"Contradiction: Fact '{query}' is implied to be both True and False.")

        if is_true:
            return True
        if is_false:
            return False
        if is_undetermined:
            return None

        return False
