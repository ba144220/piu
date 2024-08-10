from enum import Enum
from typing import List, Dict
import copy


class ElementType(Enum):
    RULE_REF = "rule_ref"
    TERMINAL = "terminal"
    END = "end"


class Element:
    def __init__(self, type: ElementType, value: str):
        self.type: ElementType = type
        self.value: str = (
            value  # if type is terminal, value is the terminal name, if type is rule_ref, value is the rule id
        )

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __str__(self):
        if self.type == ElementType.RULE_REF:
            return f"{self.value}"
        elif self.type == ElementType.TERMINAL:
            return f'"{self.value}"'
        elif self.type == ElementType.END:
            return "$"


def r(rule_id: str):
    return Element(ElementType.RULE_REF, rule_id)


def t(terminal: str):
    return Element(ElementType.TERMINAL, terminal)


def end():
    return Element(ElementType.END, "")


class Stack(list):
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
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True


def print_stacks(stacks: List[Stack]):
    for stack in stacks:
        print(stack)


class Parser:
    def __init__(self, grammar: Dict[str, List[List[Element]]], initial_rule_id: str):
        self.grammar = grammar
        self.initial_rule_id = initial_rule_id
        """
        The stacks are initialized with the first rule of the grammar. For example, if the grammar is:
        S -> aABe | bBAe
        ...
        The stacks are initialized with:
        [a,A,B,e]
        [b,B,A,e]
        """
        self.stacks: List[Stack] = []

        for seq in self.grammar[self.initial_rule_id]:
            self.stacks.append(Stack(seq))

        print("-----------------")
        print_stacks(self.stacks)
        print("Number of stacks: ", len(self.stacks))
        print("Allowed chars: ", self._get_allowed_next_chars())

    def _get_allowed_next_chars(self):
        allowed_chars = set()
        for stack in self.stacks:
            if stack.top().type == ElementType.TERMINAL:
                allowed_chars.add(stack.top().value)
            elif stack.top().type == ElementType.END:
                allowed_chars.add("<EOF>")
        return allowed_chars

    def add_char(self, char: str):
        # filter out the stacks that don't start with the char
        self.stacks = [stack for stack in self.stacks if stack.top().value == char]

        if len(self.stacks) == 0:
            raise Exception("The char is not accepted by the grammar")

        for index, stack in enumerate(self.stacks):
            stack.pop(0)

        for index, stack in enumerate(self.stacks):
            if stack.top().type == ElementType.RULE_REF:
                sequences = self.grammar[stack.top().value]
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


if __name__ == "__main__":
    """
    S -> aABe | bBAe
    A -> aA | a
    B -> bB | b
    """
    GRAMMAR = {
        "S": [[t("a"), r("A"), r("B"), end()], [t("b"), r("B"), t("a"), end()]],
        "A": [[t("a"), r("A")], [t("a")]],
        "B": [[t("b"), r("B")], [t("b")]],
    }

    """
    S -> abe
    """
    GRAMMAR = {
        "S": [[t("a"), t("b"), end()]],
    }
    """
    S->(A|(AD|(AKD|(DA|(DAD|(DAKD
    D->(A|(AK|(DA|(DAK
    A->)
    C->(
    B->(|(D
    K->(A|(AK|(DA|(AKK|(DAK|(DAKK
    """
    GRAMMAR = {
        "S": [
            [t("("), r("A"), end()],
            [t("("), r("A"), r("D"), end()],
            [t("("), r("A"), r("K"), r("D"), end()],
            [t("("), r("D"), r("A"), end()],
            [t("("), r("D"), r("A"), r("D"), end()],
            [t("("), r("D"), r("A"), r("K"), r("D"), end()],
        ],
        "D": [
            [t("("), r("A")],
            [t("("), r("A"), r("K")],
            [t("("), r("D"), r("A")],
            [t("("), r("D"), r("A"), r("K")],
        ],
        "A": [[t(")")]],
        "C": [[t("(")]],
        "B": [[t("(")], [t("("), r("D")]],
        "K": [
            [t("("), r("A")],
            [t("("), r("A"), r("K")],
            [t("("), r("D"), r("A")],
            [t("("), r("A"), r("K"), r("K")],
            [t("("), r("D"), r("A"), r("K")],
            [t("("), r("D"), r("A"), r("K"), r("K")],
        ],
    }

    INITIAL_RULE_ID = "S"
    parser = Parser(GRAMMAR, INITIAL_RULE_ID)

    string = ""
    while True:
        char = input("Enter a char: ")
        parser.add_char(char)
        string += char
        print("String: ", string)
