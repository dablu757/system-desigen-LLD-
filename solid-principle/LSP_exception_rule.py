
# Demonstrates LSP Exception Rule in Python


# -------- Custom Exceptions --------
class LogicError(Exception):
    pass


class OutOfRangeError(LogicError):
    pass


# -------- Parent Class --------
class Parent:
    def get_value(self) -> None:
        """
        Parent promises that it may raise LogicError
        """
        raise LogicError("Parent error")


# -------- Child Class (Throws Narrower Exception) --------
class Child(Parent):
    def get_value(self) -> None:
        """
        Child throws a subtype of LogicError
        (LSP compliant)
        """
        raise OutOfRangeError("Child error")


# -------- Client Code --------
def client_code(p: Parent):
    try:
        p.get_value()
    except LogicError as e:
        print(f"Client handled error: {e}")


# -------- Main Execution --------
if __name__ == "__main__":
    parent = Parent()
    child = Child()

    print("\n--- Using Parent ---")
    client_code(parent)

    print("\n--- Using Child (substituted) ---")
    client_code(child)
