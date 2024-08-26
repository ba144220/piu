from piu.grammars.converters.gnf.greibach import GreibachGrammar
from piu.grammars.converters.gnf.chomsky import ChomskyGrammar
from piu.grammars.element import (
    TerminalElement,
    RuleRefElement,
    EmptyElement,
    EndElement,
)
from piu.grammars.converters.utils import print_cnf_grammar
from piu.grammars.predictor import Predictor


def t(v):
    return TerminalElement(v)


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
    r("S"): [[t("a"), r("A"), r("B")], [t("b"), r("B"), r("A")]],
    r("A"): [[t("a"), r("A")], [t("a")]],
    r("B"): [[t("b"), r("B")], [t("b")]],
    r("C"): [[t("c")], [t("c")]],
    r("D"): [[r("E")]],
}

PARENTHESIS_GRAMMAR = {
    r("S"): [[r("S"), r("S")], [r("H1"), r("H0")], [empty()]],
    r("H0"): [[t(")")]],
    r("H1"): [[r("H2"), r("S")]],
    r("H2"): [[t("(")]],
}

PARENTHESIS_GRAMMAR = {r("S"): [[r("S"), r("S")], [t("("), r("S"), t(")")], [empty()]]}

cnf = ChomskyGrammar(PARENTHESIS_GRAMMAR, RuleRefElement("S"))

for function_name, grammar in cnf.grammar_timeline:
    print(f"======{function_name}======")
    print(grammar.non_terminals)
    print_cnf_grammar(grammar.export_grammar())

gnf = GreibachGrammar(cnf.export_grammar(), cnf.start_symbol)

for function_name, grammar in gnf.grammar_timeline:
    print(f"======{function_name}======")
    print(grammar.non_terminals)
    print_cnf_grammar(grammar.export_grammar())

predictor = Predictor(gnf.export_grammar(), gnf.start_symbol)

STRING = ""
while True:
    char = input("Enter a char: ")
    predictor.add_char(char)
    STRING += char
    print("String: ", STRING)
