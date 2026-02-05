import sys
import re


class InputHandler:

    def __init__(self, filename, knowledge_base, parser):

        self.filename = filename
        self.kb = knowledge_base
        self.parser = parser
        self.raw_rules = []
        self.raw_facts_line = None
        self.is_initial_facts_set = False
        self.is_query_set = False
        self.query_list = []


    def process_file(self):

        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

        for line_num, line in enumerate(lines, 1):
            # Remove comments
            comment_split = line.split('#')[0]
            
            # Remove whitespaces[ \t\n\r\f\v]
            clean_line = re.sub(r"\s+", "", comment_split)

            # Skip empty lines
            if not clean_line:
                continue

            # Identify Line Type
            if clean_line.startswith('='):
                self._validate_and_store_facts(clean_line, line_num)

            elif clean_line.startswith('?'):
                self._handle_query(clean_line, line_num)

            else:
                self._handle_rule(clean_line, line_num)

        if not self.is_initial_facts_set:
            print("Error: Input file is missing initial facts line (starting with '=').")
            sys.exit(1)
        if not self.is_query_set:
            print("Error: Input file is missing query line (starting with '?').")
            sys.exit(1)

        self.kb.set_initial_facts(self.raw_facts_line)

        return self.query_list


    def _validate_and_store_facts(self, line, line_num):

        if self.is_initial_facts_set:
            print(f"Error (Line {line_num}): Multiple initial fact declarations.")
            sys.exit(1)

        # Validate format (only = and uppercase letters allowed)
        if not re.match(r'^=[A-Z]*$', line):
            print(f"Error (Line {line_num}): Invalid facts format. Expected '=<upper_case_chars>'. Found: {line}")
            sys.exit(1)

        self.is_initial_facts_set = True
        self.raw_facts_line = line


    def _handle_query(self, line, line_num):

        if self.is_query_set:
            print(f"Error (Line {line_num}): Multiple query declarations found.")
            sys.exit(1)

        # Validate format (only ? and uppercase letters allowed)
        if not re.match(r'^\?[A-Z]+$', line):
            print(f"Error (Line {line_num}): Invalid query format. Expected '?<upper_case_chars>'. Found: {line}")
            sys.exit(1)

        self.query_list = list(line[1:]) # Remove '?'
        self.is_query_set = True


    def _handle_rule(self, line, line_num):
        # Character Validation
        if not re.match(r'^[A-Z()!+|^=><]+$', line):
            print(f"Error (Line {line_num}): Invalid characters in rule. Found: {line}")
            sys.exit(1)

        try:
            left, op, right = self.parser.parse_rule(line)
            
            if left is None or right is None:
                print(f"Error (Line {line_num}): Invalid rule syntax. Missing implication arrow ?")
                sys.exit(1)

            self.kb.add_rule(left, op, right)

        except ValueError as e:
            print(f"Error (Line {line_num}): {e}")
            sys.exit(1)
