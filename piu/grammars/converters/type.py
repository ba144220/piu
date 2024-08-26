from typing import List, Dict, NewType
from piu.grammars.element import RuleRefElement, Element

GeneralGrammar = NewType("GeneralGrammar", Dict[RuleRefElement, List[List[Element]]])
