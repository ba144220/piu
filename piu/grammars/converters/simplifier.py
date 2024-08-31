import copy
from typing import List, Tuple
import itertools
import inspect

from piu.grammars.converters.grammar import Grammar
from piu.grammars.converters.rule import Rule
from piu.grammars.converters.type import GeneralGrammar
from piu.grammars.element import RuleRefElement, EmptyElement
from piu.grammars.converters.utils import DEBUG


class AlterStartElement(RuleRefElement):

    def __init__(self):
        super().__init__("S'")


class SimplifiedGrammar(Grammar):

    def __init__(self, grammar: GeneralGrammar, start_symbol: RuleRefElement):
        super().__init__(grammar, start_symbol)
        self.grammar_timeline: List[Tuple[str, Grammar]] = []

    def simplify(self):
        self.add_new_start_symbol()
        self.remove_redundant_non_terminals()
        self.remove_unreachable_symbols()
        self.remove_null_productions()
        self.remove_unit_productions()
        self.sort_rules()

    def add_new_start_symbol(self):
        if self.check_start_symbol_is_used():
            new_start_symbol = AlterStartElement()
            new_rule = Rule(new_start_symbol, [self.start_symbol])
            self.rules.insert(0, new_rule)
            self.non_terminals.add(new_start_symbol)
            self.numbers += 1
            self.start_symbol = new_start_symbol

            if DEBUG:
                self.grammar_timeline.append(
                    (inspect.stack()[0][3], copy.deepcopy(self))
                )

    def check_start_symbol_is_used(self):
        for rule in self.rules:
            if self.start_symbol in rule.rhs:
                return True
        return False

    def remove_redundant_non_terminals(self):
        """
        Ｆind non-terminals that don't generate a terminal and remove rules containing them
        """
        prev_set = set()
        current_set = self.terminals.copy()
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.rules:
                # check if current rule derives any of current_set symbols
                rhs_current_set_intersection = [
                    symbol for symbol in rule.rhs if symbol in current_set
                ]
                if len(rhs_current_set_intersection) == len(rule.rhs):
                    current_set.add(rule.lhs)

        redundant_symbols = self.non_terminals.difference(current_set)

        # Remove Rules which consist of redundant symbols
        if redundant_symbols:
            self.rules = [
                rule
                for rule in self.rules
                if not rule.get_all_element().intersection(redundant_symbols)
            ]
            self.non_terminals = self.non_terminals.difference(redundant_symbols)
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def remove_unreachable_symbols(self):
        """
        Find symbols that are unreachable from starting symbol and remove rules containing them
        """
        prev_set = set()
        current_set = {self.start_symbol}
        while prev_set != current_set:
            prev_set = current_set.copy()
            for rule in self.rules:
                if rule.lhs in current_set:
                    current_set.update(rule.get_all_element())

        unreachable_symbols = self.terminals.union(self.non_terminals).difference(
            current_set
        )
        if unreachable_symbols:
            self.rules = [
                rule
                for rule in self.rules
                if not rule.get_all_element().intersection(unreachable_symbols)
            ]

            self.non_terminals = self.non_terminals.difference(unreachable_symbols)

        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def remove_null_productions(self):
        """
        Null production:
        A -> ε or A -> ... -> ε

        1- Look for all productions whose right-side contains A
        2- Replace each occurrences of A in these productions with ε
        3- Add the result productions to the grammar
        """
        nullable_non_terminals: List[RuleRefElement] = []
        while True:
            for rule in self.rules:
                if (
                    rule.lhs != self.start_symbol
                    and len(rule.rhs) == 1
                    and isinstance(rule.rhs[0], EmptyElement)
                ):
                    nullable_non_terminals.append(rule.lhs)
                    self.rules.remove(rule)
                    break
                else:
                    current_rhs_non_terminal = [
                        el for el in rule.rhs if isinstance(el, RuleRefElement)
                    ]
                    if (
                        rule.lhs not in nullable_non_terminals
                        and len(rule.rhs) == len(current_rhs_non_terminal)
                        and all(
                            t in nullable_non_terminals
                            for t in current_rhs_non_terminal
                        )
                    ):
                        nullable_non_terminals.append(rule.lhs)
                        break
            else:
                break

        for nullable_non_t in nullable_non_terminals:
            if nullable_non_t != self.start_symbol:
                self.add_new_rules_by_replacing_nullable_symbol(nullable_non_t)
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def add_new_rules_by_replacing_nullable_symbol(
        self, nullable_symbol: RuleRefElement
    ):
        for rule in self.rules:
            occ_indices = [
                index for index, sym in enumerate(rule.rhs) if sym == nullable_symbol
            ]
            # for all combinations of occurrence indices add a new rule
            combinations = []
            for i in range(1, len(occ_indices) + 1):
                combinations += list(itertools.combinations(occ_indices, i))

            for comb in combinations:
                new_rhs = [el for ind, el in enumerate(rule.rhs) if ind not in comb]
                if new_rhs:
                    self.rules.append(Rule(rule.lhs, new_rhs))

    def remove_unit_productions(self):
        """
        Unit production:
        A -> B  (A,B ∈ non-terminals)

        1- Add A -> x to grammar whenever B -> x occurs
        2- Delete A -> B from grammar
        """
        current = {}.fromkeys(sorted(self.non_terminals))
        current = {key: {key} for key in current}
        prev = {}
        while current != prev:
            prev = copy.deepcopy(current)
            for rule in self.rules:
                if rule.is_unit_production():
                    for _, unit_set in current.items():
                        if rule.lhs in unit_set:
                            unit_set.add(rule.rhs[0])

        new_rules = []
        for non_terminal_a, unit_set in current.items():
            for non_terminal_b in sorted(unit_set):
                b_rules = self[non_terminal_b]
                for rule in b_rules:
                    if not rule.is_unit_production():
                        new_rule = Rule(non_terminal_a, rule.rhs)
                        new_rules.append(new_rule)

        self.rules = [rule for rule in self.rules if not rule.is_unit_production()]

        for rule in new_rules:
            if rule not in self.rules:
                self.rules.append(rule)
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))

    def sort_rules(self):
        self.sort()
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))
