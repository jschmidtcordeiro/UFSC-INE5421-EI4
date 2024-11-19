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

    def print_first_set(self):
        for nt, first_set in self.first_set.items():
            print(f"{nt} -> {first_set}")

    def calculate_first_set(self):
        # Initialize FIRST sets for all non-terminals
        for nt in self.non_terminals:
            self.first_set[nt] = set()
            
        # Keep iterating until no changes are made
        while True:
            changes_made = False
            
            # For each production rule
            for nt, productions in self.productions.items():
                for production in productions:
                    # Case 1: Empty production
                    if production == "&":
                        if "&" not in self.first_set[nt]:
                            self.first_set[nt].add("&")
                            changes_made = True
                        continue
                    
                    # Case 2: Production starts with terminal
                    if production[0] in self.terminals:
                        if production[0] not in self.first_set[nt]:
                            self.first_set[nt].add(production[0])
                            changes_made = True
                        continue
                    
                    # Case 3: Production starts with non-terminal
                    # Add all non-epsilon symbols from FIRST set of first symbol
                    first_symbol = production[0]
                    if first_symbol in self.first_set:
                        for symbol in self.first_set[first_symbol] - {"&"}:
                            if symbol not in self.first_set[nt]:
                                self.first_set[nt].add(symbol)
                                changes_made = True
                        
                        # If first symbol can derive epsilon, continue with next symbol
                        i = 0
                        all_can_be_empty = True
                        while i < len(production) and all_can_be_empty:
                            current = production[i]
                            if current in self.terminals:
                                if current not in self.first_set[nt]:
                                    self.first_set[nt].add(current)
                                    changes_made = True
                                all_can_be_empty = False
                            elif current in self.non_terminals:
                                if "&" not in self.first_set[current]:
                                    all_can_be_empty = False
                                for symbol in self.first_set[current] - {"&"}:
                                    if symbol not in self.first_set[nt]:
                                        self.first_set[nt].add(symbol)
                                        changes_made = True
                            i += 1
                        
                        # If all symbols in production can derive epsilon
                        if all_can_be_empty and "&" not in self.first_set[nt]:
                            self.first_set[nt].add("&")
                            changes_made = True
            
            # If no changes were made in this iteration, we're done
            if not changes_made:
                break

    def calculate_follow_set(self):
        pass