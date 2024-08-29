from piu.grammars.converters.type import GeneralGrammar


DEBUG = False


def print_grammar(grammar: GeneralGrammar):
    for lhs, rhs in grammar.items():
        print(
            str(lhs)
            + "->"
            + " |".join(["".join([str(el) for el in seq]) for seq in rhs])
        )
