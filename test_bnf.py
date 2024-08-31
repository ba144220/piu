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

AST_GRAMMAR = r"""
    start: code_block

    code_block: statement+

    ?statement: if | set_var | print

    if: "if" value "{" code_block "}"
    set_var: NAME "=" value ";"
    print: "print" value ";"

    value: name | STRING | DEC_NUMBER
    name: NAME

    %import python (NAME, STRING, DEC_NUMBER)
    %import common.WS
    %ignore WS
"""

with open("examples/python2.lark", "r") as f:
    PYTHON2_GRAMMAR = f.read()

start = "file_input"

with open("examples/verilog.lark", "r") as f:
    VERILOG_GRAMMAR = f.read()

CSV_GRAMMAR = r"""
start: header _NL row+
header: "#" " "? (WORD _SEPARATOR?)+
row: (_anything _SEPARATOR?)+ _NL
_anything: INT | WORD | NON_SEPARATOR_STRING | FLOAT | SIGNED_FLOAT
NON_SEPARATOR_STRING: /[a-zA-z.;\\\/]+/
_SEPARATOR: /[  ]+/
          | "\t"
          | ","

%import common.NEWLINE -> _NL
%import common.WORD
%import common.INT
%import common.FLOAT
%import common.SIGNED_FLOAT
"""

MULTIPLE3_GRAMMAR = r"""
start: mod0mod0+
mod0mod0: "0" | "1" mod1mod0
mod1mod0: "1" | "0" mod2mod1 mod1mod0
mod2mod1: "0" | "1" mod2mod1
"""

with open("examples/lark.lark", "r") as f:
    LARK_GRAMMAR = f.read()

start = "value"
bnf = BackusGrammar(JSON_GRAMMAR, start=start)

print("=====BNF=====")

print_grammar(bnf.export_grammar())

print("=====CNF=====")

cnf = ChomskyGrammar(bnf.export_grammar(), bnf.start_symbol)

for function_name, grammar in cnf.grammar_timeline:
    print(f"======{function_name}======")
    print_grammar(grammar.export_grammar())

print_grammar(cnf.export_grammar())

print("=====GNF=====")

gnf = GreibachGrammar(cnf.export_grammar(), cnf.start_symbol)

for function_name, grammar in gnf.grammar_timeline:
    print(f"======{function_name}======")
    print(grammar.reverse_mapping)
    print_grammar(grammar.export_grammar())

print_grammar(gnf.export_grammar())
