"""
INTERFACE SEGREGATION PRINCIPLE (ISP)

Definition:
Clients should not be forced to depend on methods they do not use.

Below:
1️⃣ ISP VIOLATED example (Bad design)
2️⃣ ISP FOLLOWED example (Correct design)
"""

from abc import ABC, abstractmethod


# =========================================================
# ❌ ISP VIOLATED (BAD DESIGN)
# =========================================================

class Shape(ABC):
    """
    Fat interface ❌
    Forces all shapes to implement both area() and volume()
    """

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def volume(self) -> float:
        pass  # ❌ Not applicable for 2D shapes


class Square(Shape):
    """
    Square is a 2D shape
    But forced to implement volume() ❌
    """

    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side * self.side

    def volume(self) -> float:
        # ❌ Wrong: Square has no volume
        raise Exception("Volume not applicable for Square")


class Rectangle(Shape):
    """
    Rectangle is also a 2D shape
    But forced to implement volume() ❌
    """

    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width

    def area(self) -> float:
        return self.length * self.width

    def volume(self) -> float:
        # ❌ Wrong: Rectangle has no volume
        raise Exception("Volume not applicable for Rectangle")


"""
WHY THIS IS BAD ❌
- 2D shapes are forced to implement unnecessary methods
- Runtime exceptions indicate poor design
- Violates Interface Segregation Principle
"""


# =========================================================
# ✅ ISP FOLLOWED (GOOD DESIGN)
# =========================================================

class Shape2D(ABC):
    """
    Interface for 2D shapes only ✅
    """

    @abstractmethod
    def area(self) -> float:
        pass


class Shape3D(ABC):
    """
    Interface for 3D shapes only ✅
    """

    @abstractmethod
    def volume(self) -> float:
        pass


class Square2D(Shape2D):
    """
    Square implements only what it needs ✅
    """

    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side * self.side


class Rectangle2D(Shape2D):
    """
    Rectangle implements only area() ✅
    """

    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width

    def area(self) -> float:
        return self.length * self.width


class Cube(Shape2D, Shape3D):
    """
    Cube is a 3D shape
    Implements both area() and volume() correctly ✅
    """

    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return 6 * self.side * self.side

    def volume(self) -> float:
        return self.side ** 3


"""
WHY THIS IS GOOD ✅
- Small, focused interfaces
- No forced methods
- No runtime exceptions
- Easy to extend
- Perfectly follows ISP
"""


# =========================================================
# TESTING (Optional)
# =========================================================
if __name__ == "__main__":
    square = Square2D(4)
    print("Square area:", square.area())

    rectangle = Rectangle2D(5, 3)
    print("Rectangle area:", rectangle.area())

    cube = Cube(3)
    print("Cube area:", cube.area())
    print("Cube volume:", cube.volume())
