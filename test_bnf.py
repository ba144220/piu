from piu.grammars.converters.bnf.backus import BackusGrammar
from piu.grammars.converters.cnf.chomsky import ChomskyGrammar
from piu.grammars.converters.gnf.greibach import GreibachGrammar
from piu.grammars.converters.utils import print_grammar

JSON_GRAMMAR = r"""
    value: dict
         | list
         | ESCAPED_STRING
         | SIGNED_NUMBER
         | "true" | "false" | "null"

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"
    pair : ESCAPED_STRING ":" value

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    """

bnf = BackusGrammar(JSON_GRAMMAR, start="value")

print("=====BNF=====")

print_grammar(bnf.export_grammar())

print("=====CNF=====")

cnf = ChomskyGrammar(bnf.export_grammar(), bnf.start_symbol)

for function_name, grammar in cnf.grammar_timeline:
    print(f"======{function_name}======")
    print(grammar.non_terminals)
    print_grammar(grammar.export_grammar())

print_grammar(cnf.export_grammar())

print("=====GNF=====")

gnf = GreibachGrammar(cnf.export_grammar(), cnf.start_symbol)

for function_name, grammar in gnf.grammar_timeline:
    print(f"======{function_name}======")
    print(grammar.non_terminals)
    print_grammar(grammar.export_grammar())


print_grammar(gnf.export_grammar())
