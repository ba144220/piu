from typing import List, Set, Union
from piu.grammars.element import Element, RuleRefElement


class ElementList(list):
    def __init__(self, l: Union[List[Element], "ElementList"]):
        super().__init__(l)

    def __hash__(self) -> int:
        return hash(tuple(self))


class Rule:
    def __init__(self, lhs: RuleRefElement, rhs: Union[List[Element], ElementList]):
        self.lhs = lhs
        self.rhs = ElementList(rhs)

    def get_all_element(self) -> Set[Element]:
        return set([self.lhs] + self.rhs)

    def is_unit_production(self) -> bool:
        return len(self.rhs) == 1 and isinstance(self.rhs[0], RuleRefElement)

    def __str__(self):
        return str(self.lhs) + "  ->  " + "".join([str(el) for el in self.rhs])

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "Rule") -> bool:
        return self.lhs == other.lhs and self.rhs == other.rhs
