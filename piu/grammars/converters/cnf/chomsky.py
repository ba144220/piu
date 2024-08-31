import copy
import inspect
from typing import List, Dict
from piu.grammars.converters.simplifier import SimplifiedGrammar
from piu.grammars.converters.rule import Rule, ElementList
from piu.grammars.converters.type import GeneralGrammar
from piu.grammars.converters.utils import DEBUG
from piu.grammars.element import RuleRefElement, EmptyElement, TerminalElement, Element


class ChomskyGrammar(SimplifiedGrammar):

    def __init__(self, grammar: GeneralGrammar, start_symbol: RuleRefElement):
        super().__init__(grammar, start_symbol)

        self.add_new_start_symbol()
        self.remove_null_productions()
        self.remove_unit_productions()
        self.convert()
        self.remove_redundant_non_terminals()
        self.remove_unreachable_symbols()
        self.sort_rules()

    # pylint: disable=too-many-branches
    def convert(self):

        singles: Dict[TerminalElement, RuleRefElement] = {}
        multis: Dict[List[Element], RuleRefElement] = {}

        for lhs in sorted(self.non_terminals):
            rules = self[lhs]
            if len(rules) == 1 and len(rules[0].rhs) == 1:
                term = rules[0].rhs[0]
                if not isinstance(term, EmptyElement) and isinstance(
                    term, TerminalElement
                ):
                    singles[term] = lhs

            if len(rules) == 1:
                multis[rules[0].rhs] = lhs
        # pylint: disable=too-many-nested-blocks
        non_terminals = sorted(list(self.non_terminals))
        for lhs in non_terminals:
            rules = self[lhs]
            for rule in rules:
                if len(rule.rhs) == 2:
                    for index, el in enumerate(rule.rhs):
                        if isinstance(el, TerminalElement):
                            if el not in singles:
                                new_non_terminal = RuleRefElement(f"RRE_{self.numbers}")
                                self.numbers += 1
                                non_terminals.append(new_non_terminal)
                                self.rules.append(Rule(new_non_terminal, [el]))
                                singles[el] = new_non_terminal
                            rule.rhs[index] = singles[el]

                elif len(rule.rhs) > 2:
                    last = rule.rhs[-1]
                    if isinstance(last, TerminalElement):
                        if last not in singles:
                            new_non_terminal = RuleRefElement(f"RRE_{self.numbers}")
                            self.numbers += 1
                            non_terminals.append(new_non_terminal)
                            self.rules.append(Rule(new_non_terminal, [last]))
                            singles[last] = new_non_terminal
                        rule.rhs[-1] = singles[last]
                    term = ElementList(rule.rhs[:-1])
                    if term not in multis:
                        new_non_terminal = RuleRefElement(f"RRE_{self.numbers}")
                        self.numbers += 1
                        non_terminals.append(new_non_terminal)
                        self.rules.append(Rule(new_non_terminal, term))
                        multis[term] = new_non_terminal
                    self.rules.append(Rule(lhs, [multis[term], last]))
                    self.rules.remove(rule)

        self.non_terminals = set(non_terminals)
        if DEBUG:
            self.grammar_timeline.append((inspect.stack()[0][3], copy.deepcopy(self)))
