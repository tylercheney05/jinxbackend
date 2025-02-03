import os

import pandas as pd
import pytz
from django.db import transaction

from cups.models import Cup
from flavors.models import Flavor
from jinxbackend.settings import BASE_DIR
from locations.models import Location
from menuitems.models import MenuItem
from orders.models import (
    CustomOrder,
    CustomOrderFlavor,
    CustomOrderFlavorCustomOrder,
    Discount,
    Order,
    OrderDiscount,
    OrderItem,
    OrderItemCustomOrder,
    OrderItemMenuItem,
    OrderPaidAmount,
)
from sodas.models import Soda
from users.models import User


def run():
    file_location = os.path.join(BASE_DIR, "files", "Order Tracking.xlsx")
    menu_item_orders = pd.read_excel(file_location, sheet_name="Menu Item Orders")
    custom_orders = pd.read_excel(file_location, sheet_name="BYO Orders")

    cup_mapping = {
        "16 oz": "16",
        "32 oz": "32",
    }

    with transaction.atomic():
        try:
            free_discount, _ = Discount.objects.get_or_create(name="Free", code="FREE")

            ## Add Menu Item Orders
            prev_order_num = 0
            for label, row in menu_item_orders.iterrows():
                order_num = row["Order #"]
                date = row["Date"]
                location = row["Location"]
                cup = row["Cup"].strip()
                zero_sugar = row["Zero Sugar"]
                menu_item = row["Menu Item"]
                charged = row["Charged"]
                discount_code = row["Discount Code"]

                location_obj = Location.objects.get(name=location)
                cup_obj = Cup.objects.get(size=cup_mapping[cup])
                menu_item_obj = MenuItem.objects.get(name__iexact=menu_item)

                if order_num != prev_order_num:
                    total_charged = charged
                    date = date.to_pydatetime()
                    pacific = pytz.timezone("US/Pacific")
                    utc = pytz.utc
                    date = pacific.localize(date).astimezone(utc)

                    order = Order.objects.create(
                        date=date,
                        collected_by=User.objects.first(),
                        is_paid=True,
                        location=location_obj,
                        is_complete=True,
                        is_in_progress=False,
                    )
                    print(f"Order {order_num} created")

                    OrderPaidAmount.objects.create(
                        order=order, paid_amount=total_charged
                    )
                    print(f"OrderPaidAmount {order_num} ${total_charged} created")
                else:
                    total_charged += charged
                    OrderPaidAmount.objects.filter(order=order).update(
                        paid_amount=total_charged
                    )
                    print(f"OrderPaidAmount {order_num} ${total_charged} updated")

                order_item = OrderItem.objects.create(
                    order=order, cup=cup_obj, low_sugar=zero_sugar
                )
                print(f"OrderItem {order_num} {menu_item} created")

                OrderItemMenuItem.objects.create(
                    order_item=order_item, menu_item=menu_item_obj
                )
                print(f"OrderItemMenuItem {order_num} {menu_item} created")

                if pd.notna(discount_code):
                    discount = Discount.objects.get(code=discount_code)
                    OrderDiscount.objects.create(order=order, discount=discount)
                    print(f"OrderDiscount {order_num} {discount_code} created")
                elif charged == 0:
                    OrderDiscount.objects.create(order=order, discount=free_discount)
                    print(f"OrderDiscount {order_num} FREE created")

                prev_order_num = order_num

            print("\n")
            print("--------------------")
            print("\n")

            ## Add Custom Orders
            prev_order_num = 0
            for label, row in custom_orders.iterrows():
                order_num = row["Order #"]
                date = row["Date"]
                location = row["Location"]
                cup = row["Cup"].strip()
                zero_sugar = row["Zero Sugar"]
                soda = row["Soda"].strip()
                flavor1 = row["Flavor 1"]
                flavor2 = row["Flavor 2"]
                flavor3 = row["Flavor 3"]
                flavor4 = row["Flavor 4"]
                charged = row["Charged"]

                location_obj = Location.objects.get(name=location)
                cup_obj = Cup.objects.get(size=cup_mapping[cup])
                soda_obj = Soda.objects.get(name=soda)

                flavor1 = (
                    Flavor.objects.get(name=flavor1) if pd.notna(flavor1) else None
                )
                flavor2 = (
                    Flavor.objects.get(name=flavor2) if pd.notna(flavor2) else None
                )
                flavor3 = (
                    Flavor.objects.get(name=flavor3) if pd.notna(flavor3) else None
                )
                flavor4 = (
                    Flavor.objects.get(name=flavor4) if pd.notna(flavor4) else None
                )

                if order_num != prev_order_num:
                    total_charged = charged
                    date = date.to_pydatetime()
                    pacific = pytz.timezone("US/Pacific")
                    utc = pytz.utc
                    date = pacific.localize(date).astimezone(utc)

                    order = Order.objects.create(
                        date=date,
                        collected_by=User.objects.first(),
                        is_paid=True,
                        location=location_obj,
                        is_complete=True,
                        is_in_progress=False,
                    )
                    print(f"Order {order_num} created")

                    OrderPaidAmount.objects.create(
                        order=order, paid_amount=total_charged
                    )
                    print(f"OrderPaidAmount {order_num} ${total_charged} created")
                else:
                    total_charged += charged
                    OrderPaidAmount.objects.filter(order=order).update(
                        paid_amount=total_charged
                    )
                    print(f"OrderPaidAmount {order_num} ${total_charged} updated")

                order_item = OrderItem.objects.create(
                    order=order, cup=cup_obj, low_sugar=zero_sugar
                )
                print(f"OrderItem {order_num} Custom Order created")

                custom_order = CustomOrder.objects.create(
                    soda=soda_obj,
                )
                print(f"CustomOrder {order_num} created")

                OrderItemCustomOrder.objects.create(
                    order_item=order_item, custom_order=custom_order
                )
                print(f"OrderItemCustomOrder {order_num} created")

                quantity_mapping = {
                    "16 oz": 1,
                    "32 oz": 2,
                }

                if flavor1:
                    custom_flavor1 = CustomOrderFlavor.objects.create(
                        flavor=flavor1, quantity=quantity_mapping[cup]
                    )
                    CustomOrderFlavorCustomOrder.objects.create(
                        custom_order_flavor=custom_flavor1, custom_order=custom_order
                    )
                    print(f"CustomOrderFlavor {order_num} {flavor1} created")
                if flavor2:
                    custom_flavor2 = CustomOrderFlavor.objects.create(
                        flavor=flavor2, quantity=quantity_mapping[cup]
                    )
                    CustomOrderFlavorCustomOrder.objects.create(
                        custom_order_flavor=custom_flavor2, custom_order=custom_order
                    )
                    print(f"CustomOrderFlavor {order_num} {flavor2} created")
                if flavor3:
                    custom_flavor3 = CustomOrderFlavor.objects.create(
                        flavor=flavor3, quantity=quantity_mapping[cup]
                    )
                    CustomOrderFlavorCustomOrder.objects.create(
                        custom_order_flavor=custom_flavor3, custom_order=custom_order
                    )
                    print(f"CustomOrderFlavor {order_num} {flavor3} created")
                if flavor4:
                    custom_flavor4 = CustomOrderFlavor.objects.create(
                        flavor=flavor4, quantity=quantity_mapping[cup]
                    )
                    CustomOrderFlavorCustomOrder.objects.create(
                        custom_order_flavor=custom_flavor4, custom_order=custom_order
                    )
                    print(f"CustomOrderFlavor {order_num} {flavor4} created")

                if charged == 0:
                    OrderDiscount.objects.create(order=order, discount=free_discount)
                    print(f"OrderDiscount {order_num} FREE created")

        except Exception as e:
            print("\n")
            print("Error", e)
            print("Location", location)
            raise e
