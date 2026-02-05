import re


class Parser:

    def __init__(self):
        # Define operators, precedence, associativity
        self.operators = {
            '!': {'prec': 4, 'assoc': 'right'}, # NOT
            '+': {'prec': 3, 'assoc': 'left'},  # AND
            '|': {'prec': 2, 'assoc': 'left'},  # OR
            '^': {'prec': 1, 'assoc': 'left'},  # XOR
            '=>': {'prec': 0, 'assoc': 'right'}, # IMPLIES
            '<=>': {'prec': 0, 'assoc': 'right'} # IFF
        }


    def _check_missing_operators(self, tokens):
        """
        Validates that there are explicit operators between facts/groups.
        Prevents syntax like 'AB', 'A(B)', ')A', or 'A!B'.
        """
        for i in range(len(tokens) - 1):
            curr = tokens[i]
            nxt = tokens[i + 1]

            # Term Endings: Facts (A-Z) or ')'
            is_term_end = (curr.isupper() and len(curr) == 1) or curr == ')'

            # Term Starts: Facts (A-Z), '(', or '!'
            is_term_start = (nxt.isupper() and len(nxt) == 1) or nxt == '(' or nxt == '!'

            if is_term_end and is_term_start:
                raise ValueError(f"Missing operator between '{curr}' and '{nxt}'")


    def tokenize(self, expression):
        """
        Splits string into a list of tokens.
        Example: "A + B => C" -> ['A', '+', 'B', '=>', 'C']
        """
        # Remove comments
        expression = expression.split('#')[0].strip()

        token_pattern = r'<=>|=>|[A-Z()!+|^]'
        tokens = re.findall(token_pattern, expression)
        return tokens


    def rpn(self, tokens):
        """
        Converts tokens to Reverse Polish Notation (RPN).
        Example: ['A', '+', 'B', '|', 'C'] -> ['A', 'B', '+', 'C', '|']
        """
        output_queue = []
        operator_stack = []

        for token in tokens:
            # Facts : ex : 'A'
            if token.isupper() and len(token) == 1:
                output_queue.append(token)

            # Operators : ex : '+', '=>'
            elif token in self.operators:
                while (operator_stack and operator_stack[-1] != '(' and
                       (
                           # If operator at top of stack has greater precedence
                           (self.operators[operator_stack[-1]]['prec'] > self.operators[token]['prec']) or
                           # Or equal precedence and left associative
                           (self.operators[operator_stack[-1]]['prec'] == self.operators[token]['prec'] and
                            self.operators[token]['assoc'] == 'left')
                            # And last operator_stack is not '('
                       )):
                    # Pop this operator from operator_stack and append it to output_queue
                    output_queue.append(operator_stack.pop())

                # Append operator token to operator_stack
                operator_stack.append(token)

            # Open parenthesis : '('
            elif token == '(':
                operator_stack.append(token)

            # Close parenthesis : ')'
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    # Pop everything until '(' from operator_stack and append to output_queue
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    # When '(', discard parenthesis
                    operator_stack.pop() # Discard open parenthesis
                else:
                    raise ValueError("Mismatched parenthesis")

        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parenthesis")
            # Append the remaining operators from operator_stack to output_queue
            output_queue.append(operator_stack.pop())

        return output_queue


    def parse_rule(self, line):
        """
        Splits a rule line into left and right and converts both to RPN.
        Example: "A + B => C"
        Returns: (['A', 'B', '+'], ['C'])
        """
        tokens = self.tokenize(line)

        # Check for missing operators
        self._check_missing_operators(tokens)

        # Split tokens into left and right based on implies/iff (=>/<=>)
        if '<=>' in tokens:
            split_idx = tokens.index('<=>')
            operator_type = '<=>'
        elif '=>' in tokens:
            split_idx = tokens.index('=>')
            operator_type = '=>'
        else:
            return None, None, None # Not a rule (maybe initial facts or query)

        left_tokens = tokens[:split_idx]
        right_tokens = tokens[split_idx+1:]

        if not left_tokens or not right_tokens:
            raise ValueError(f"Incomplete rule : Missing a side.")

        # RPN application on both sides
        left_rpn = self.rpn(left_tokens)
        right_rpn = self.rpn(right_tokens)

        return left_rpn, operator_type, right_rpn
