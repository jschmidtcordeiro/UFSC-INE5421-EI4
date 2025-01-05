"""
Alunos:
  Gabriel Reimann Cervi (22204117)
  João Pedro Schmidt Cordeiro (22100628)
"""

from grammar import Grammar

def main():

    input = "P = KVC; K = cK; K = &; V = vV; V = F; F = fPiF; F = &; C = bVCe; C = miC; C = &;"

    grammar = Grammar.from_string_EI4(input)
    # grammar.print_productions()
    grammar.calculate_first_set()
    # grammar.print_first_set()
    grammar.calculate_follow_set()
    # grammar.print_follow_set()
    grammar.print_output_EI4()
if __name__ == "__main__":
    main()
