from piu.grammars.converters.type import CNFGrammar


DEBUG = False


def print_cnf_grammar(grammar: CNFGrammar):
    for lhs, rhs in grammar.items():
        print(
            str(lhs)
            + "->"
            + " |".join(["".join([str(el) for el in seq]) for seq in rhs])
        )
