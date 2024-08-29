from lark import Lark

from piu.grammars.converters.rule import Rule
from piu.grammars.element import RuleRefElement, TerminalElement
from piu.grammars.converters.grammar import Grammar


class BackusGrammar(Grammar):

    def __init__(self, bnf_grammar: str, start: str):

        self.start = start
        super().__init__(bnf_grammar, RuleRefElement(start))

    def build_rules(self, grammar: str):

        parser = Lark(grammar, start=self.start)

        lark_terminals_dict = {t.name: t for t in parser.terminals}

        self.rules = [
            Rule(
                RuleRefElement(lark_rule.origin.name),
                [
                    (
                        TerminalElement(
                            lark_symbol.name, lark_terminals_dict[lark_symbol.name]
                        )
                        if lark_symbol.is_term
                        else RuleRefElement(lark_symbol.name)
                    )
                    for lark_symbol in lark_rule.expansion
                ],
            )
            for lark_rule in parser.rules
        ]
