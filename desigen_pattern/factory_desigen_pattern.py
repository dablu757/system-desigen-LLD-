from abc import ABC, abstractmethod


# ==========================================================
# 1️⃣ SIMPLE FACTORY
# ==========================================================

class SimpleBurger(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass


class BasicBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Basic Burger")


class StandardBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Standard Burger")


class PremiumBurger(SimpleBurger):
    def prepare(self) -> None:
        print("Preparing Premium Burger")


class SimpleBurgerFactory:

    _burger_map = {
        "basic": BasicBurger,
        "standard": StandardBurger,
        "premium": PremiumBurger,
    }

    @staticmethod
    def create_burger(burger_type: str) -> SimpleBurger:
        burger_class = SimpleBurgerFactory._burger_map.get(burger_type.lower())

        if not burger_class:
            raise ValueError(f"Invalid burger type: {burger_type}")

        return burger_class()


# ==========================================================
# 2️⃣ FACTORY METHOD
# ==========================================================

class Burger(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass


# ---------- Regular Burgers ----------

class RegularBasicBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Basic Burger")


class RegularStandardBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Standard Burger")


class RegularPremiumBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Premium Burger")


# ---------- Wheat Burgers ----------

class WheatBasicBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Basic Burger")


class WheatStandardBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Standard Burger")


class WheatPremiumBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Premium Burger")


# ---------- Abstract Factory ----------

class BurgerFactory(ABC):

    @abstractmethod
    def create_burger(self, burger_type: str) -> Burger:
        pass


# ---------- Concrete Factory 1 ----------

class SinghBurgerFactory(BurgerFactory):

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


# ---------- Concrete Factory 2 ----------

class KingBurgerFactory(BurgerFactory):

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
# 3️⃣ CLIENT CODE
# ==========================================================

# if __name__ == "__main__":

#     print("=== Simple Factory ===")
#     burger = SimpleBurgerFactory.create_burger("basic")
#     burger.prepare()

#     print("\n=== Factory Method ===")
#     factory = SinghBurgerFactory()
#     burger = factory.create_burger("premium")
#     burger.prepare()

#     factory = KingBurgerFactory()
#     burger = factory.create_burger("standard")
#     burger.prepare()



    from abc import ABC, abstractmethod


# ==========================================================
# 3 ABSTRACT FACTORY DESIGEN 
# ==========================================================

class Burger(ABC):
    @abstractmethod
    def prepare(self) -> None:
        pass


class Drink(ABC):
    @abstractmethod
    def serve(self) -> None:
        pass


# ==========================================================
# 2️⃣ REGULAR PRODUCT FAMILY
# ==========================================================

# Burgers
class RegularBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Regular Burger")


# Drinks
class RegularDrink(Drink):
    def serve(self) -> None:
        print("Serving Regular Cold Drink")


# ==========================================================
# 3️⃣ WHEAT PRODUCT FAMILY
# ==========================================================

# Burgers
class WheatBurger(Burger):
    def prepare(self) -> None:
        print("Preparing Wheat Burger")


# Drinks
class WheatDrink(Drink):
    def serve(self) -> None:
        print("Serving Healthy Wheat Smoothie")


# ==========================================================
# 4️⃣ ABSTRACT FACTORY
# ==========================================================

class RestaurantFactory(ABC):

    @abstractmethod
    def create_burger(self) -> Burger:
        pass

    @abstractmethod
    def create_drink(self) -> Drink:
        pass


# ==========================================================
# 5️⃣ CONCRETE FACTORIES
# ==========================================================

class SinghRestaurantFactory(RestaurantFactory):

    def create_burger(self) -> Burger:
        return RegularBurger()

    def create_drink(self) -> Drink:
        return RegularDrink()


class KingRestaurantFactory(RestaurantFactory):

    def create_burger(self) -> Burger:
        return WheatBurger()

    def create_drink(self) -> Drink:
        return WheatDrink()


# ==========================================================
# 6️⃣ CLIENT CODE
# ==========================================================

def serve_customer(factory: RestaurantFactory) -> None:
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