import src.nodes as n


class KnowledgeBase:

    def __init__(self):
        # Dict to store fact nodes.
        # Key: 'A', Value: FactNode object
        self.nodes = {}
        self.refreshed_nodes = {}


    def get_refreshed_node(self, char):
        """
        Singleton retrieval: If node exists, return it. 
        If not, create it, register it, and return it.
        """
        if char not in self.refreshed_nodes:
            self.refreshed_nodes[char] = n.FactNode(char)
        return self.refreshed_nodes[char]


    def get_node(self, char):
        """
        Singleton retrieval: If node exists, return it. 
        If not, create it, register it, and return it.
        """
        if char not in self.nodes:
            self.nodes[char] = n.FactNode(char)
        return self.nodes[char]


    def _link_rule(self, left, right):
        """
        Creates a RuleNode and links it to the relevant FactNodes.
        """
        rule = n.RuleNode(left, right)
        # Link this rule to every FactNode appearing in the right.
        for symbol in right:
             if symbol.isupper() and len(symbol) == 1:
                 node = self.get_node(symbol)
                 node.implying_rules.append(rule)


    def add_rule(self, left, operator, right):
        """
        Adds a rule to the graph.
        Handles the split of Biconditional (<=>) rules automatically.
        """
        # Get symbols from rule
        for token in left + right:
            if token.isupper() and len(token) == 1:
                self.get_node(token)

        # MANDATORY: Standard Implication (=>)
        if operator == '=>':
            self._link_rule(left, right)

        # BONUS: Biconditional (<=>) 
        # "A <=> B" = "A => B" AND "B => A"
        elif operator == '<=>':
            self._link_rule(left, right) # Forward
            self._link_rule(right, left) # Backward


    def set_initial_facts(self, facts_str):
        """
        Parses the initial facts string (e.g., "=ABC").
        Sets these to True. All others default to False.
        """
        # Set to default
        for node in self.nodes.values():
            node.value = False
            node.is_true_by_default = False

        # Set initial facts to True (ex: "=ABC")
        clean_facts = facts_str.replace('=', '').strip()
        for char in clean_facts:
            if char.isupper():
                node = self.get_node(char)
                node.value = True
                node.is_true_by_default = True


    def add_facts(self, facts_str):
        """
        Parses the added facts string (e.g., "=ABC").
        Sets these to True.
        """
        # Set added facts to True (ex: "=ABC")
        clean_facts = facts_str.replace('=', '').strip()
        for char in clean_facts:
            if char.isupper():
                node = self.get_node(char)
                node.value = True
                node.is_true_by_default = True


    def rm_facts(self, facts_str):
        """
        Parses the rm facts string (e.g., "-ABC").
        Sets these to False.
        """
        # Set rm facts to False (ex: "-ABC")
        clean_facts = facts_str.replace('-', '').strip()
        for char in clean_facts:
            if char.isupper():
                node = self.get_node(char)
                node.value = False
                node.is_true_by_default = False


    def dump_graphviz(self):
        """
        Generates a .dot format file to visualize the graph.
        """
        filename = "graph.dot"
        
        try:
            with open(filename, "w") as f:
                f.write("digraph ExpertSystem {\n")
                f.write("    rankdir=LR;\n")
                f.write("    node [shape=circle];\n")
                for name, node in self.refreshed_nodes.items():
                    if node.is_true_by_default:
                        color = "green"
                        style = "filled"
                    elif node.value is True:
                        color = "cyan"
                        style = "filled"
                    elif node.value is False:
                        color = "red"
                        style = "filled"
                    else:
                        color = "yellow"
                        style = "filled"
                    f.write(f"    {name} [style=\"{style}\", fillcolor=\"{color}\"];\n")
                    for rule in node.implying_rules:
                        lhs_label = "".join(rule.left)
                        f.write(f"    \"{lhs_label}\" -> {name};\n")
                f.write("}\n")
            print(f"Graphviz file generated: {filename}")

        except IOError as e:
            print(f"Error writing file: {e}")


    # More readable print
    def __str__(self):
        return f"Graph Nodes: {len(self.nodes)} symbols loaded."
