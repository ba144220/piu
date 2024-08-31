from piu.grammars.element import (
    TerminalElement,
    RuleRefElement,
    EmptyElement,
    EndElement,
)
from piu.grammars.parser import Parser
from piu.grammars.converters.gnf.greibach import GreibachGrammar


def t(v):
    return TerminalElement(v, None)


def r(v):
    return RuleRefElement(v)


def empty():
    return EmptyElement()


def end():
    return EndElement()


"""
S -> aABe | bBAe
A -> aA | a
B -> bB | b
"""
GRAMMAR = {
    r("S"): [[t("a"), r("A"), r("B"), end()], [t("b"), r("B"), t("a"), end()]],
    r("A"): [[t("a"), r("A")], [t("a")]],
    r("B"): [[t("b"), r("B")], [t("b")]],
}

"""
S -> abe
"""
GRAMMAR = {
    r("S"): [[t("a"), t("b"), end()]],
}
"""
S->(A|(AD|(AKD|(DA|(DAD|(DAKD
D->(A|(AK|(DA|(DAK
A->)
C->(
B->(|(D
K->(A|(AK|(DA|(AKK|(DAK|(DAKK
"""
GRAMMAR = {
    r("S"): [
        [t("("), r("A")],
        [t("("), r("A"), r("D")],
        [t("("), r("A"), r("K"), r("D")],
        [t("("), r("D"), r("A")],
        [t("("), r("D"), r("A"), r("D")],
        [t("("), r("D"), r("A"), r("K"), r("D")],
    ],
    r("D"): [
        [t("("), r("A")],
        [t("("), r("A"), r("K")],
        [t("("), r("D"), r("A")],
        [t("("), r("D"), r("A"), r("K")],
    ],
    r("A"): [[t(")")]],
    r("C"): [[t("(")]],
    r("B"): [[t("(")], [t("("), r("D")]],
    r("K"): [
        [t("("), r("A")],
        [t("("), r("A"), r("K")],
        [t("("), r("D"), r("A")],
        [t("("), r("A"), r("K"), r("K")],
        [t("("), r("D"), r("A"), r("K")],
        [t("("), r("D"), r("A"), r("K"), r("K")],
    ],
}
"""
S->SS
"""
INVALID_GRAMMER = {r("S"): [[r("S"), r("S")]]}

"""
S -> SS | H1H0 | ϵ
H0 -> )
H1 -> H2S
H2 -> (
"""
PARENTHESIS_CNF_GRAMMAR = {
    r("S"): [[r("S"), r("S")], [r("H1"), r("H0")], [empty()]],
    r("H0"): [[t(")")]],
    r("H1"): [[r("H2"), r("S")]],
    r("H2"): [[t("(")]],
}

INITIAL_RULE_ID = r("S")

if __name__ == "__main__":
    # gnf = GreibachGrammar(PARENTHESIS_CNF_GRAMMAR, r("S"))
    # PARENTHESIS_GNF_GRAMMAR = gnf.export_grammar()
    parser = Parser(GRAMMAR, r("S"))

    STRING = ""
    while True:
        char = input("Enter a char: ")
        parser.add_char(char)
        STRING += char
        print("String: ", STRING)
