class Element:

    def __init__(self, value: str):
        self.value: str = value

    def __eq__(self, other: "Element"):
        # pylint: disable=unidiomatic-typecheck
        return type(self) == type(other) and self.value == other.value

    def __gt__(self, other: "Element"):
        return str(type(self)) + self.value > str(type(other)) + other.value

    def __str__(self):
        return f" {self.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.value + str(type(self)))


class RuleRefElement(Element):
    """Element for rule_ref"""


class TerminalElement(Element):
    """Element for terminal"""


class EndElement(Element):
    """Element for end"""

    def __init__(self):
        super().__init__("$")


class EmptyElement(TerminalElement):
    """Element for empty"""

    def __init__(self):
        super().__init__("ε")
