from typing import List, Dict, NewType
from piu.grammars.element import RuleRefElement, Element

CNFGrammar = NewType("CNFGrammar", Dict[RuleRefElement, List[List[Element]]])
