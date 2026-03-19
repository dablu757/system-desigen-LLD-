from abc import ABC, abstractmethod


# ==========================================================
# 1️⃣ SIMPLE FACTORY PATTERN
# ==========================================================
"""
Simple Factory:
- Centralizes object creation logic.
- Client does NOT instantiate concrete classes directly.
- Uses mapping/conditional logic inside a single factory.
- Not an official GoF pattern.
"""


# ----------------- Product Interface -----------------
class SimpleBurger(ABC):
    """
    Abstract Product:
    Defines the common interface for all burger types.
    """

    @abstractmethod
    def prepare(self) -> None:
        pass


# ----------------- Concrete Products -----------------
class BasicBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Basic Burger")


class StandardBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Standard Burger")


class PremiumBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Premium Burger")


# ----------------- Factory Class -----------------
class SimpleBurgerFactory:
    """
    Responsible for object creation.
    Uses dictionary mapping instead of if-else.
    """

    _burger_map = {
        "basic": BasicBurger,
        "standard": StandardBurger,
        "premium": PremiumBurger,
    }

    @staticmethod
    def create_burger(burger_type: str) -> SimpleBurger:
        """
        Returns appropriate Burger instance
        based on input type.
        """
        burger_class = SimpleBurgerFactory._burger_map.get(
            burger_type.lower()
        )

        if not burger_class:
            raise ValueError(f"Invalid burger type: {burger_type}")

        return burger_class()


# ==========================================================
# 2️⃣ FACTORY METHOD PATTERN
# ==========================================================
"""
Factory Method (GoF Pattern):
- Defines an interface for creating objects.
- Subclasses decide which concrete product to instantiate.
- Replaces large conditional logic with polymorphism.
"""


# ----------------- Product Interface -----------------
class Burger(ABC):
    """
    Common interface for all burgers.
    """

    @abstractmethod
    def prepare(self) -> None:
        pass


# ----------------- Regular Product Family -----------------
class RegularBasicBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Basic Burger")


class RegularStandardBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Standard Burger")


class RegularPremiumBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Premium Burger")


# ----------------- Wheat Product Family -----------------
class WheatBasicBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Basic Burger")


class WheatStandardBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Standard Burger")


class WheatPremiumBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Premium Burger")


# ----------------- Abstract Factory (Creator) -----------------
class BurgerFactory(ABC):
    """
    Declares the Factory Method.
    Subclasses implement object creation logic.
    """

    @abstractmethod
    def create_burger(self, burger_type: str) -> Burger:
        pass


# ----------------- Concrete Factory 1 -----------------
class SinghBurgerFactory(BurgerFactory):
    """
    Responsible for creating Wheat burger family.
    """

    _burger_map = {
        "basic": WheatBasicBurger,
        "standard": WheatStandardBurger,
        "premium": WheatPremiumBurger,
    }

    def create_burger(self, burger_type: str) -> Burger:
        burger_class = self._burger_map.get(burger_type.lower())

        if not burger_class:
            raise ValueError(f"Invalid burger type: {burger_type}")

        return burger_class()


# ----------------- Concrete Factory 2 -----------------
class KingBurgerFactory(BurgerFactory):
    """
    Responsible for creating Regular burger family.
    """

    _burger_map = {
        "basic": RegularBasicBurger,
        "standard": RegularStandardBurger,
        "premium": RegularPremiumBurger,
    }

    def create_burger(self, burger_type: str) -> Burger:
        burger_class = self._burger_map.get(burger_type.lower())

        if not burger_class:
            raise ValueError(f"Invalid burger type: {burger_type}")

        return burger_class()


# ==========================================================
# 3️⃣ ABSTRACT FACTORY PATTERN
# ==========================================================
"""
Abstract Factory:
- Creates families of related objects.
- Ensures compatibility within a product family.
- No conditional logic in client code.
- Fully polymorphic and scalable.
"""


# ----------------- Abstract Products -----------------
class Drink(ABC):
    @abstractmethod
    def serve(self) -> None:
        pass


# ----------------- Regular Product Family -----------------
class RegularBurgerAF(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Burger (AF)")


class RegularDrink(Drink):
    def serve(self) -> None:
        print("Serving Regular Cold Drink")


# ----------------- Wheat Product Family -----------------
class WheatBurgerAF(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Burger (AF)")


class WheatDrink(Drink):
    def serve(self) -> None:
        print("Serving Healthy Wheat Smoothie")


# ----------------- Abstract Factory -----------------
class RestaurantFactory(ABC):
    """
    Abstract Factory declares methods to create
    multiple related products.
    """

    @abstractmethod
    def create_burger(self) -> Burger:
        pass

    @abstractmethod
    def create_drink(self) -> Drink:
        pass


# ----------------- Concrete Factories -----------------
class SinghRestaurantFactory(RestaurantFactory):
    """
    Creates Regular product family.
    """

    def create_burger(self) -> Burger:
        return RegularBurgerAF()

    def create_drink(self) -> Drink:
        return RegularDrink()


class KingRestaurantFactory(RestaurantFactory):
    """
    Creates Wheat product family.
    """

    def create_burger(self) -> Burger:
        return WheatBurgerAF()

    def create_drink(self) -> Drink:
        return WheatDrink()


# ----------------- Client Code -----------------
def serve_customer(factory: RestaurantFactory) -> None:
    """
    Client depends only on abstract factory.
    Completely decoupled from concrete classes.
    """
    burger = factory.create_burger()
    drink = factory.create_drink()

    burger.prepare()
    drink.serve()
    print("-" * 40)


if __name__ == "__main__":

    print("Singh Restaurant Order")
    serve_customer(SinghRestaurantFactory())

    print("King Restaurant Order")
    serve_customer(KingRestaurantFactory())