from __future__ import annotations

from datetime import UTC, datetime, timedelta

from LLD_food_delivery_app.factories import NowOrderFactory, ScheduledOrderFactory
from LLD_food_delivery_app.models import MenuItem, Restaurant, User
from LLD_food_delivery_app.services import NotificationService, OrderManager, RestaurantManager
from LLD_food_delivery_app.strategies import NetBanking, UPI


def demo() -> None:
    # Setup sample restaurants and menu
    rm = RestaurantManager()
    dominos = Restaurant(
        id=1,
        name="Dominos",
        address="Indiranagar, Bangalore",
        menu_items=[
            MenuItem(code=101, name="Margherita", price=199.0),
            MenuItem(code=102, name="Veg Loaded", price=299.0),
        ],
    )
    rm.add_restaurant(dominos)

    # User adds items to cart
    user = User(id=10, name="Aman", address="HSR Layout, Bangalore")
    user.cart.add_to_cart(dominos, dominos.menu_items[0])
    user.cart.add_to_cart(dominos, dominos.menu_items[1])

    # Create immediate delivery order
    now_factory = NowOrderFactory()
    order1 = now_factory.create_order(
        order_id=5001,
        user=user,
        restaurant=dominos,
        items=list(user.cart.items),
        payment_strategy=UPI("aman@upi"),
        order_type="delivery",
    )

    if order1.payment_strategy.pay(order1.amount):
        om = OrderManager()
        om.add_order(order1)
        NotificationService().notify(order1)

    # Create scheduled pickup order
    scheduled_factory = ScheduledOrderFactory()
    order2 = scheduled_factory.create_order(
        order_id=5002,
        user=user,
        restaurant=dominos,
        items=list(user.cart.items),
        payment_strategy=NetBanking("HDFC"),
        order_type="pickup",
        scheduled_at=datetime.now(UTC) + timedelta(minutes=45),
    )

    if order2.payment_strategy.pay(order2.amount):
        om = OrderManager()
        om.add_order(order2)
        NotificationService().notify(order2)

    print(f"Total orders for user {user.id}: {len(OrderManager().list_user_orders(user.id))}")


if __name__ == "__main__":
    demo()
