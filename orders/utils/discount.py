from decimal import Decimal
from typing import Optional

from orders.constants import ORDER_ITEMS_ATTRS
from orders.models import Discount, DiscountCupSize, Order


def calculate_order_price_with_discount(order: Order, discount: Discount) -> Decimal:
    discount_percent_off = 0
    discount_price = 0
    discount_cup_size = None
    if discount:
        if hasattr(discount, "discountcupsize"):
            discount_cup_size = discount.discountcupsize.cup
        if hasattr(discount, "discountpercentoff"):
            discount_percent_off = discount.discountpercentoff.percent_off
        elif hasattr(discount, "discountprice"):
            discount_price = discount.discountprice.price

    if discount_percent_off:
        return calculate_order_price_with_discount_percent_off(
            order, discount_percent_off, discount_cup_size
        )
    elif discount_price:
        return calculate_order_price_with_discount_price(
            order, discount_price, discount_cup_size
        )
    return order.pending_price


def calculate_order_price_with_discount_percent_off(
    order: Order,
    discount_percent_off: int,
    discount_cup_size: Optional[DiscountCupSize],
) -> Decimal:
    price = 0
    for item in order.items.all():
        if discount_cup_size and discount_cup_size != item.cup:
            for attr in ORDER_ITEMS_ATTRS:
                if hasattr(item, attr):
                    price += getattr(item, attr).price
                    break
        else:
            for attr in ORDER_ITEMS_ATTRS:
                if hasattr(item, attr):
                    price += getattr(item, attr).price * (1 - discount_percent_off)
                    break
    return price


def calculate_order_price_with_discount_price(
    order: Order, discount_price: Decimal, discount_cup_size: Optional[DiscountCupSize]
) -> Decimal:
    price = 0
    for item in order.items.all():
        if discount_cup_size and discount_cup_size != item.cup:
            for attr in ORDER_ITEMS_ATTRS:
                if hasattr(item, attr):
                    price += getattr(item, attr).price
                    break
        else:
            price += discount_price
    return price
