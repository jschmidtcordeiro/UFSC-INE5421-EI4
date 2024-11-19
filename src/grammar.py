class Grammar:
    def __init__(self, non_terminals, terminals, initial_symbol, productions):
        # self.non_terminals = ['A', 'B', 'S']
        # self.terminals = ['a', 'b', 'c', 'd']
        # self.initial_symbol = S
        # self.productions = {'S': ['Bd', '&'], 'B': ['Bc', 'b', 'Ab'], 'A': ['Sa', 'a']}
        # self.first_set = {'S': ['a', 'b', 'c', 'd'], 'B': ['b', 'c', 'd'], 'A': ['a']}
        # self.follow_set = {'S': ['a', 'b', 'c', 'd'], 'B': ['b', 'c', 'd'], 'A': ['a']}
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.initial_symbol = initial_symbol
        self.productions = productions
        self.first_set = {}
        self.follow_set = {}

    def __str__(self):
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nInitial symbol: {self.initial_symbol}\nProductions: {self.productions}"

    @classmethod
    def from_string_EI4(cls, input_str):
        # Extract all symbols from the input string
        production_strings = input_str.split(";")
        productions = {}
        non_terminals = set()
        terminals = set()
        
        # First pass: collect non-terminals (they appear on the left side of productions)
        for prod in production_strings:
            if "=" in prod:
                left, _ = prod.split("=")
                non_terminals.add(left.strip())
        
        # Second pass: process productions and collect terminals
        for prod in production_strings:
            if "=" in prod:
                left, right = prod.split("=")
                left = left.strip()
                right = right.strip()
                
                # Add symbols that aren't non-terminals to terminals set
                for char in right:
                    if char not in non_terminals and char != " " and char != "&":
                        terminals.add(char)
                
                # Initialize list if key doesn't exist, then append
                if left not in productions:
                    productions[left] = []
                productions[left].append(right)
        
        # Use first non-terminal in the first production as initial symbol
        initial_symbol = next(iter(non_terminals))
        
        return cls(list(non_terminals), list(terminals), initial_symbol, productions)

    def print_productions(self):
        # Print initial symbol first
        if self.initial_symbol in self.productions:
            productions_str = " | ".join(self.productions[self.initial_symbol])
            print(f"    {self.initial_symbol} -> {productions_str}")

        # Print remaining symbols in alphabetical order
        for symbol in sorted(self.productions.keys()):
            if symbol != self.initial_symbol:
                productions_str = " | ".join(self.productions[symbol])
                print(f"    {symbol} -> {productions_str}")

    def calculate_first_set(self):
        pass

    def calculate_follow_set(self):
        pass