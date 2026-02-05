"""
E-commerce Product & Shopping Cart Implementation
With proper validation, edge cases, and error handling
"""


# -------- Custom Exceptions --------
class InvalidPriceError(Exception):
    pass


class EmptyCartError(Exception):
    pass


# -------- Product --------
class Product:
    """
    Responsible only for product data
    """

    def __init__(self, name: str, price: float) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string")

        if not isinstance(price, (int, float)) or price <= 0:
            raise InvalidPriceError("Product price must be greater than 0")

        self.name = name
        self.price = float(price)


# -------- Shopping Cart --------
class ShoppingCart:
    """
    Responsible for holding products and calculating total price
    """

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to cart")

        self.products.append(product)

    def remove_product(self, product_name: str) -> None:
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                return

        raise ValueError(f"Product '{product_name}' not found in cart")

    def calculate_total_price(self) -> float:
        if not self.products:
            raise EmptyCartError("Cannot calculate total. Cart is empty")

        return sum(product.price for product in self.products)

    def is_empty(self) -> bool:
        return len(self.products) == 0


# -------- Invoice Printer --------
class CartInvoicePrinter:
    """
    Responsible only for printing invoice
    """

    def __init__(self, cart: ShoppingCart):
        self.cart = cart

    def print_invoice(self) -> None:
        if self.cart.is_empty():
            print("Invoice cannot be generated. Cart is empty ❌")
            return

        print("\n----- INVOICE -----")
        for product in self.cart.products:
            print(f"{product.name} : ₹{product.price:.2f}")
        print("-------------------")

        try:
            total = self.cart.calculate_total_price()
            print(f"Total: ₹{total:.2f}")
        except EmptyCartError as e:
            print(e)


# -------- Database Storage --------
class CartDBStorage:
    """
    Responsible only for persistence logic
    """

    def __init__(self, cart: ShoppingCart):
        self.cart = cart

    def save_to_db(self) -> None:
        if self.cart.is_empty():
            print("Cart is empty. Nothing to save ❌")
            return

        print("\nSaving cart to database...")
        for product in self.cart.products:
            print(f"Saved {product.name} - ₹{product.price:.2f}")

        print("Cart saved successfully ✅")


# -------- Main Execution --------
if __name__ == "__main__":
    try:
        cart = ShoppingCart()

        cart.add_product(Product("Laptop", 60000))
        cart.add_product(Product("Mouse", 800))
        cart.add_product(Product("Keyboard", 1500))

        invoice = CartInvoicePrinter(cart)
        invoice.print_invoice()

        db_storage = CartDBStorage(cart)
        db_storage.save_to_db()

    except (InvalidPriceError, ValueError, TypeError) as e:
        print(f"Error: {e}")
