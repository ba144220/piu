from typing import List, Set

from piu.grammars.element import RuleRefElement, TerminalElement, EndElement
from piu.grammars.converters.type import CNFGrammar
from piu.grammars.converters.gnf.rule import Rule


class Grammar:
    def __init__(self, grammar: CNFGrammar, start_symbol: RuleRefElement):
        self.rules: List[Rule] = []
        self.build_rules(grammar)
        self.start_symbol = start_symbol
        self.terminals: Set[TerminalElement] = set()
        self.non_terminals: Set[RuleRefElement] = set()
        self.detect_symbols()

    def __getitem__(self, lhs: RuleRefElement) -> List[Rule]:
        return [r for r in self.rules if r.lhs == lhs]

    def build_rules(self, grammar: CNFGrammar):
        self.split_rules(grammar)

    def split_rules(self, grammar: CNFGrammar):
        """
        split rules with more than 1 right-hand-side to multiple rules with 1 right-hand-side
        example:
        A -> a | b | c
        will be converted to:
        A -> a
        A -> b
        A -> c
        """
        self.rules = [Rule(lhs, rhs[0]) for lhs, rhs in grammar.items()]

        for lhs, rhs in grammar.items():
            if len(rhs) > 1:
                for seq in rhs[1:]:
                    self.rules.append(Rule(lhs, seq))

    def detect_symbols(self):
        for rule in self.rules:
            self.non_terminals.add(rule.lhs)
            for el in rule.rhs:
                if isinstance(el, TerminalElement):
                    self.terminals.add(el)
                else:
                    self.non_terminals.add(el)

    def export_grammar(self) -> CNFGrammar:
        grammar = {}

        for rule in self.rules:
            if rule.lhs not in grammar:
                grammar[rule.lhs] = set([rule.rhs])
            else:
                grammar[rule.lhs].add(rule.rhs)

        result = {k: list(v) for k, v in grammar.items()}
        print(result)
        result[self.start_symbol] = [
            seq + [EndElement()] for seq in result[self.start_symbol]
        ]

        return result

    def sort(self):
        s_productions = self[self.start_symbol]
        other_productions = [rule for rule in self.rules if rule not in s_productions]
        self.rules = s_productions + other_productions
