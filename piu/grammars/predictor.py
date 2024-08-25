from typing import List, Dict
import copy
from piu.grammars.element import Element, TerminalElement, RuleRefElement, EndElement
from piu.exceptions.base import GrammarException


class Stack(list):
    """
    A stack data structure used to represent rules in GNF
    """

    def __init__(self, elements: List[Element]):
        super().__init__(elements)

    def push(self, element: Element):
        """
        Init: [a, b, c]
        push(d)
        Result: [d, a, b, c]
        """
        self.insert(0, element)

    def push_multiple(self, elements: List[Element]):
        """
        Init: [a, b, c]
        push_multiple([d, e, f])
        Result: [d, e, f, a, b, c]
        """
        for el in reversed(elements):
            self.push(el)

    def top(self):
        return self[0]

    def __str__(self):
        return f"[{', '.join([str(el) for el in self])}]"

    def __eq__(self, other: "Stack"):
        if len(self) != len(other):
            return False

        for s, o in zip(self, other):
            if s != o:
                return False
        return True


def print_stacks(stacks: List[Stack]):
    for stack in stacks:
        print(stack)


class Predictor:
    """
    A next char predictor using GNF grammar
    """

    def __init__(
        self, grammar: Dict[RuleRefElement, List[Stack]], initial_rule: RuleRefElement
    ):
        self.grammar = grammar

        if not self._validate_gnf():
            raise GrammarException("The grammar is not GNF")

        self.initial_rule = initial_rule
        """
        The stacks are initialized with the first rule of the grammar. For example, if the grammar is:
        S -> aABe | bBAe
        ...
        The stacks are initialized with:
        [a,A,B,e]
        [b,B,A,e]
        """
        self.stacks: List[Stack] = []

        for seq in self.grammar[self.initial_rule]:
            self.stacks.append(Stack(seq))

        print("-----------------")
        print_stacks(self.stacks)
        print("Number of stacks: ", len(self.stacks))
        print("Allowed chars: ", self._get_allowed_next_chars())

    def _validate_gnf(self):
        for seqs in self.grammar.values():
            for seq in seqs:
                if isinstance(seq[0], RuleRefElement):
                    return False
                for i in range(1, len(seq)):
                    if isinstance(seq[i], TerminalElement):
                        return False
        return True

    def _get_allowed_next_chars(self):
        allowed_chars = set()
        for stack in self.stacks:
            if isinstance(stack.top(), TerminalElement):
                allowed_chars.add(stack.top().value)
            elif isinstance(stack.top(), EndElement):
                allowed_chars.add("<EOF>")
        return allowed_chars

    def add_char(self, char: str):
        """
        Filter out the stacks that don't start with the char
        """
        self.stacks = [stack for stack in self.stacks if stack.top().value == char]

        if len(self.stacks) == 0:
            raise GrammarException("The char is not accepted by the grammar")

        for index, stack in enumerate(self.stacks):
            stack.pop(0)

        for index, stack in enumerate(self.stacks):
            if isinstance(stack.top(), RuleRefElement):
                sequences = self.grammar[stack.top()]
                stack.pop(0)
                old_stack = copy.deepcopy(stack)
                # delete the old stack
                self.stacks.pop(index)
                for seq in sequences:
                    new_stack = Stack(seq + old_stack)
                    # If there is a stack that is equal to the old stack, we don't need to add it again
                    if new_stack not in self.stacks:
                        self.stacks.insert(index, new_stack)

        print("-----------------")
        print_stacks(self.stacks)
        print("Number of stacks: ", len(self.stacks))
        print("Allowed chars: ", self._get_allowed_next_chars())
