from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta

from LLD_food_delivery_app.factories import NowOrderFactory, ScheduledOrderFactory
from LLD_food_delivery_app.models import Cart, DeliveryOrder, MenuItem, PickupOrder, Restaurant, User
from LLD_food_delivery_app.services import OrderManager, RestaurantManager
from LLD_food_delivery_app.strategies import NetBanking, UPI


class TestFoodDeliveryLLD(unittest.TestCase):
    def setUp(self) -> None:
        # Reset singleton instances so tests remain isolated.
        RestaurantManager._instance = None
        OrderManager._instance = None

        self.rest1 = Restaurant(
            id=1,
            name="Dominos",
            address="Indiranagar, Bangalore",
            menu_items=[
                MenuItem(code=101, name="Margherita", price=199.0),
                MenuItem(code=102, name="Veg Loaded", price=299.0),
            ],
        )
        self.rest2 = Restaurant(
            id=2,
            name="KFC",
            address="Koramangala, Bangalore",
            menu_items=[MenuItem(code=201, name="Zinger", price=249.0)],
        )
        self.user = User(id=10, name="Aman", address="HSR Layout, Bangalore")

    def test_cart_allows_single_restaurant_only(self) -> None:
        cart = Cart()
        cart.add_to_cart(self.rest1, self.rest1.menu_items[0])

        with self.assertRaises(ValueError):
            cart.add_to_cart(self.rest2, self.rest2.menu_items[0])

    def test_cart_total_and_clear(self) -> None:
        cart = Cart()
        cart.add_to_cart(self.rest1, self.rest1.menu_items[0])
        cart.add_to_cart(self.rest1, self.rest1.menu_items[1])

        self.assertAlmostEqual(cart.total, 498.0)
        self.assertFalse(cart.is_empty())

        cart.clear()
        self.assertTrue(cart.is_empty())
        self.assertIsNone(cart.restaurant)

    def test_now_factory_creates_delivery_order(self) -> None:
        factory = NowOrderFactory()
        order = factory.create_order(
            order_id=5001,
            user=self.user,
            restaurant=self.rest1,
            items=list(self.rest1.menu_items),
            payment_strategy=UPI("aman@upi"),
            order_type="delivery",
        )

        self.assertIsInstance(order, DeliveryOrder)
        self.assertEqual(order.get_type(), "DELIVERY")
        self.assertAlmostEqual(order.amount, 498.0)

    def test_now_factory_rejects_scheduled_at(self) -> None:
        factory = NowOrderFactory()

        with self.assertRaises(ValueError):
            factory.create_order(
                order_id=5001,
                user=self.user,
                restaurant=self.rest1,
                items=list(self.rest1.menu_items),
                payment_strategy=UPI("aman@upi"),
                order_type="pickup",
                scheduled_at=datetime.now(UTC) + timedelta(minutes=10),
            )

    def test_scheduled_factory_requires_future_time(self) -> None:
        factory = ScheduledOrderFactory()

        with self.assertRaises(ValueError):
            factory.create_order(
                order_id=5002,
                user=self.user,
                restaurant=self.rest1,
                items=list(self.rest1.menu_items),
                payment_strategy=NetBanking("HDFC"),
                order_type="pickup",
                scheduled_at=datetime.now(UTC) - timedelta(minutes=1),
            )

    def test_scheduled_factory_creates_pickup_order(self) -> None:
        factory = ScheduledOrderFactory()
        pickup_time = datetime.now(UTC) + timedelta(minutes=30)
        order = factory.create_order(
            order_id=5003,
            user=self.user,
            restaurant=self.rest1,
            items=list(self.rest1.menu_items),
            payment_strategy=NetBanking("HDFC"),
            order_type="pickup",
            scheduled_at=pickup_time,
        )

        self.assertIsInstance(order, PickupOrder)
        self.assertEqual(order.get_type(), "PICKUP")
        self.assertEqual(order.pickup_time, pickup_time)

    def test_restaurant_manager_singleton_and_search(self) -> None:
        r1 = RestaurantManager()
        r2 = RestaurantManager()

        self.assertIs(r1, r2)

        r1.add_restaurant(self.rest1)
        r1.add_restaurant(self.rest2)
        result = r2.search_by_location("indiranagar")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)

    def test_order_manager_singleton_and_user_orders(self) -> None:
        now_factory = NowOrderFactory()
        order1 = now_factory.create_order(
            order_id=6001,
            user=self.user,
            restaurant=self.rest1,
            items=list(self.rest1.menu_items),
            payment_strategy=UPI("aman@upi"),
            order_type="delivery",
        )

        other_user = User(id=20, name="Riya", address="BTM, Bangalore")
        order2 = now_factory.create_order(
            order_id=6002,
            user=other_user,
            restaurant=self.rest1,
            items=[self.rest1.menu_items[0]],
            payment_strategy=UPI("riya@upi"),
            order_type="pickup",
        )

        om1 = OrderManager()
        om2 = OrderManager()

        self.assertIs(om1, om2)

        om1.add_order(order1)
        om2.add_order(order2)

        user_orders = om1.list_user_orders(self.user.id)
        self.assertEqual(len(user_orders), 1)
        self.assertEqual(user_orders[0].id, 6001)

        fetched = om1.get_order(6002)
        self.assertEqual(fetched.user.id, 20)

    def test_payment_strategies_return_success(self) -> None:
        self.assertTrue(UPI("aman@upi").pay(100.0))
        self.assertTrue(NetBanking("HDFC").pay(200.0))


if __name__ == "__main__":
    unittest.main()
