"""
This module contains the HalfParser class, it tells if a subsequent string is accepted by a grammar or not
"""

from dataclasses import dataclass
from piu.grammars.converters.type import GeneralGrammar
from piu.grammars.element import RuleRefElement, TerminalElement, Element


@dataclass
class State:
    rule_ref: Element
    seq_index: int
    ele_index: int


class HalfParser:
    """
    A half parser is a parser that can tell if a subsequent string is accepted by a grammar or not
    """

    def __init__(self, grammar: GeneralGrammar, initial_rule: RuleRefElement):
        self.grammar = grammar
        self.initial_rule = initial_rule
        self.state = [State(rule_ref=self.initial_rule, seq_index=0, ele_index=0)]

    def add_char(self, char: str):
        self._parse_element(char)

    def _parse_element(self, char: str):
        current_state = self.state[-1]
        rule_ref = current_state.rule_ref
        seq_index = current_state.seq_index
        ele_index = current_state.ele_index

        curr_element = self.grammar[rule_ref][seq_index][ele_index]

        if isinstance(curr_element, TerminalElement):
            if curr_element.value == char:
                self.state.append(
                    State(
                        rule_ref=rule_ref, seq_index=seq_index, ele_index=ele_index + 1
                    )
                )
            else:
                self.state.append(
                    State(rule_ref=rule_ref, seq_index=seq_index, ele_index=ele_index)
                )
        elif isinstance(curr_element, RuleRefElement):
            next_rule_ref = self.grammar[curr_element][0][0]
            self.state.append(State(rule_ref=next_rule_ref, seq_index=0, ele_index=0))
            self._parse_element(char)
        else:
            raise ValueError(f"Invalid element type: {type(curr_element)}")

    def _parse_sequence(self, char: str):
        pass
