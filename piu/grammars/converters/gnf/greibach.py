import copy
import inspect
from typing import List, Dict
from piu.grammars.converters.simplifier import SimplifiedGrammar
from piu.grammars.converters.rule import Rule
from piu.grammars.converters.type import GeneralGrammar
from piu.grammars.converters.utils import DEBUG, print_grammar
from piu.grammars.element import RuleRefElement, TerminalElement


class GreibachGrammar(SimplifiedGrammar):

    def __init__(self, grammar: GeneralGrammar, start_symbol: RuleRefElement):
        super().__init__(grammar, start_symbol)

        self.mapping: Dict[RuleRefElement, int] = {}
        self.reverse_mapping: Dict[int, RuleRefElement] = {}

        self.simplify()
        self.convert()

    def convert(self):

        self.map_non_terminal_to_ordered_symbols()
        self.sort_rules_gnf()
        self.remove_left_recursion()
        self.make_rhs_first_symbol_terminal()
        self.sort_rules()
        self.simplify()

    def map_non_terminal_to_ordered_symbols(self):
        """
        Assign a value "i" for non-terminals with ascending order
        """
        cur = 0
        for rule in self.rules:
            for el in rule.get_all_element_order():
                if isinstance(el, RuleRefElement) and el not in self.mapping:
                    self.mapping[el] = cur
                    self.reverse_mapping[cur] = el
                    cur += 1

    def sort_rules_gnf(self):
        """
        Alter the rules so that the non-terminals are in ascending order, such that if a production s of form
        Ai -> Aj x, then i < j
        """

        for _, lhs in self.reverse_mapping.items():
            
            while True:
                rules = self[lhs]

                for rule in rules:
                    if isinstance(rule.rhs[0], RuleRefElement) and self.mapping[lhs] > self.mapping[rule.rhs[0]]:

                        matched_rules = self[rule.rhs[0]]

                        for matched_rule in matched_rules:
                            if matched_rule.lhs != matched_rule.rhs[0]:
                                new_rule = Rule(rule.lhs, matched_rule.rhs + rule.rhs[1:])
                                self.rules.append(new_rule)

                        self.rules.remove(rule)
                        break
                else:
                    break
                        
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def remove_left_recursion(self):
        while True:
            for rule in self.rules:
                if isinstance(rule.rhs[0], RuleRefElement) and rule.lhs == rule.rhs[0]:
                    # Find all recursive rules with same lhs
                    recursive_rules = [r for r in self[rule.lhs] if r.lhs == r.rhs[0]]

                    new_symbols: List[RuleRefElement] = []
                    for rec_rule in recursive_rules:
                        new_non_terminal = RuleRefElement(
                            f"RRE_{self.numbers}"
                        )
                        self.numbers+=1
                        self.non_terminals.add(new_non_terminal)
                        self.mapping[new_non_terminal] = len(self.mapping)
                        self.reverse_mapping[len(self.reverse_mapping)] = (
                            new_non_terminal
                        )
                        new_symbols.append(new_non_terminal)
                        self.rules.append(Rule(new_non_terminal, rec_rule.rhs[1:]))
                        self.rules.append(
                            Rule(
                                new_non_terminal, rec_rule.rhs[1:] + [new_non_terminal]
                            )
                        )

                    self.rules = [
                        rule for rule in self.rules if rule not in recursive_rules
                    ]

                    for sym in new_symbols:
                        lhs_alternative_rules = self[rule.lhs]
                        for r in lhs_alternative_rules:
                            self.rules.append(Rule(rule.lhs, r.rhs + [sym]))

                    break
            else:
                break
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))


    def make_rhs_first_symbol_terminal(self):

        while True:
            for rule in self.rules:
                if isinstance(rule.rhs[0], RuleRefElement):
                    cur_rules = self[rule.rhs[0]]
                    for cur_rule in cur_rules:
                        new_rule = Rule(rule.lhs, cur_rule.rhs + rule.rhs[1:])
                        self.rules.append(new_rule)
                    self.rules.remove(rule)
                    break
            else:
                break

        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def export_grammar(self) -> GeneralGrammar:
        
        grammar = super().export_grammar()

        lhs_terminal_mapping = {}

        for lhs, rhss in grammar.copy().items():
            if len(rhss) == 1 and len(rhss[0]) == 1 and isinstance(rhss[0][0], TerminalElement):
                lhs_terminal_mapping[lhs] = rhss[0][0]
                del grammar[lhs]

        for lhs, rhss in grammar.items():
            for rhs in rhss:
                for i, el in enumerate(rhs):
                    if isinstance(el, RuleRefElement) and el in lhs_terminal_mapping:
                        rhs[i] = lhs_terminal_mapping[el]

            grammar[lhs] = sorted(set(rhss))

        return grammar
