# Demonstrates Liskov Substitution Principle
# and Return-Type Covariance in Python


# -------- Domain Model --------
class Animal:
    """Base Animal class"""
    pass


class Dog(Animal):
    """Dog is a subtype of Animal"""
    pass


# -------- Parent Class --------
class Parent:
    def get_animal(self) -> Animal:
        print("Parent : Returning Animal instance")
        return Animal()


# -------- Child Class (Covariant Return Type) --------
class Child(Parent):
    def get_animal(self) -> Dog:
        print("Child : Returning Dog instance")
        return Dog()


# -------- Client Code --------
def client_code(p: Parent) -> None:
    """
    Client depends only on Parent.
    LSP guarantees Child can safely replace Parent.
    """
    animal = p.get_animal()
    print(f"Client received: {type(animal).__name__}")


# -------- Main Execution --------
if __name__ == "__main__":
    parent = Parent()
    child = Child()

    print("\n--- Using Parent ---")
    client_code(parent)

    print("\n--- Using Child (substituted) ---")
    client_code(child)
