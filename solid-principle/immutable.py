'''
Interview-Ready Lines
    ->Python doesn't enforce immutability like Java or C++. 
      We achieve it through design patterns, most commonly using @dataclass(frozen=True).”

    ->Final methods in Python are conventionally enforced using typing.final for static analysis.”
----------------------------------------
Key Takeaways
    1. Python favors design discipline over strict enforcement

    2. @dataclass(frozen=True) is the gold standard

    3. Avoid mutation instead of blocking it aggressively

    4. Immutability supports LSP and thread safety
------------------------------------------
One-Line Memory Rule
    “In Python, immutability is a design choice, not a keyword.”
'''


from dataclasses import dataclass
#immutable calass in python
@dataclass(frozen=True)
class User:
    id: int
    name: str


#static method in python
from typing import final
class Parent:
    @final
    def process(self):
        pass

